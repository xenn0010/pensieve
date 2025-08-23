#!/usr/bin/env python3

import argparse
import csv
import logging
import os
import re
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from jinja2 import Environment, FileSystemLoader, select_autoescape
from tenacity import (retry, stop_after_attempt, wait_exponential, 
                       retry_if_exception_type)
from tqdm import tqdm

# --- Configuration and Setup ---

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("outbox.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Scopes required for Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# --- Auth Module (auth.py functionality integrated here for simplicity) ---

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

def get_gmail_service():
    """
    Authenticates with Gmail API via OAuth 2.0.
    Loads credentials from credentials.json, saves/refreshes token.json.
    Returns an authenticated Gmail API service object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not Path(CREDENTIALS_FILE).exists():
                logger.error(f"{CREDENTIALS_FILE} not found. Please download it from Google Cloud Console.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Error building Gmail API service: {e}")
        sys.exit(1)


# --- Mailer Module (mailer.py functionality integrated here for simplicity) ---

def strip_html_tags(html_content: str) -> str:
    """Strips HTML tags to create a plain-text version of the email."""
    text = re.sub(r'<[^>]+>', '', html_content)
    return text.strip()


def create_message(
    sender_email: str,
    recipient_email: str,
    subject: str,
    html_content: str,
    plain_text_content: str
) -> dict:
    """Create a message for the Gmail API.
    Returns an object containing a base64url encoded email object.
    """
    message = MIMEMultipart("alternative")
    message["To"] = recipient_email
    message["From"] = sender_email
    message["Subject"] = subject

    message.attach(MIMEText(plain_text_content, "plain"))
    message.attach(MIMEText(html_content, "html"))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}

# --- Main Logic (gmail_send.py) ---

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10),
       retry=retry_if_exception_type(HttpError))
def send_gmail_api_message(service, user_id, message_body):
    """Sends a message via the Gmail API with retry logic."""
    try:
        message = service.users().messages().send(userId=user_id, body=message_body).execute()
        logger.debug(f"Message Id: {message['id']}")
        return message
    except HttpError as error:
        if error.resp.status in {429, 500, 502, 503, 504}: # Retry on these codes
            raise error # Re-raise to trigger tenacity retry
        else: # Don't retry on other 4xx errors (e.g., 400 Bad Request)
            logger.error(f"Permanent API error: {error}")
            raise # Don't retry, just log and fail

def write_outbox_csv(data: dict, mode: str = 'a'):
    """Writes email sending results to outbox.csv."""
    file_exists = Path("outbox.csv").exists()
    with open("outbox.csv", mode, newline='') as f:
        fieldnames = ["timestamp", "email", "subject", "status", "error_message"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or mode == 'w':
            writer.writeheader()
        writer.writerow(data)

def main():
    parser = argparse.ArgumentParser(description="Gmail API Email Sender CLI")
    parser.add_argument("--csv", default="contacts.csv", help="Path to the contacts CSV file.")
    parser.add_argument("--template", default="template.html", help="Path to the HTML email template.")
    parser.add_argument("--subject", required=True, help="Subject of the email (Jinja2 templated). ")
    parser.add_argument("--from", dest="sender_name_email", default="", 
                        help="Sender name and email (e.g., 'Helen <you@gmail.com>'). Default is authenticated user.")
    parser.add_argument("--rate", type=int, default=60, help="Emails per hour for rate limiting.")
    parser.add_argument("--start", type=int, default=1, help="Starting row in the CSV (1-indexed, inclusive).")
    parser.add_argument("--end", type=int, help="Ending row in the CSV (1-indexed, inclusive).")
    parser.add_argument("--test-to", help="Render row 1 and send one test email to this address, then exit.")
    parser.add_argument("--dry-run", action="store_true", help="Render emails and save as .eml files to ./previews/, but do not send.")
    parser.add_argument("--retries", type=int, default=3, help="Max retries for sending failed emails (exponential backoff on 429/5xx). ")
    parser.add_argument("--i-know-what-im-doing", action="store_true",
                        help="Required to send more than 100 emails in one run.")

    args = parser.parse_args()

    # Load .env variables (FROM_NAME can be overridden by --from)
    load_dotenv()
    from_name_env = os.getenv("FROM_NAME", "")
    if not args.sender_name_email:
        args.sender_name_email = from_name_env

    # Set up Jinja2 environment for template rendering
    template_dir = Path(args.template).parent if Path(args.template).parent != Path(".") else Path(".")
    template_name = Path(args.template).name
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
        undefined=SilentUndefined # Fallback to empty string for missing template variables
    )
    try:
        html_template = env.get_template(template_name)
    except Exception as e:
        logger.error(f"Error loading template {args.template}: {e}")
        sys.exit(1)
    
    # Subject templating environment
    subject_env = Environment(loader=FileSystemLoader("."), undefined=SilentUndefined)
    subject_template = subject_env.from_string(args.subject)

    # Authenticate with Gmail API
    service = None
    if not args.dry_run:
        service = get_gmail_service()

    # Read contacts CSV
    try:
        contacts_df = pd.read_csv(args.csv)
        # Apply start and end row filters (1-indexed to 0-indexed for pandas)
        start_idx = args.start - 1
        end_idx = args.end if args.end else len(contacts_df)
        contacts_df = contacts_df.iloc[start_idx:end_idx]
    except FileNotFoundError:
        logger.error(f"Contacts CSV file not found: {args.csv}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading CSV file {args.csv}: {e}")
        sys.exit(1)

    if contacts_df.empty:
        logger.info("No contacts to process in the specified range.")
        sys.exit(0)

    # Safety check for large sends
    if len(contacts_df) > 100 and not args.i_know_what_im_doing:
        logger.error("Sending to more than 100 recipients requires --i-know-what-im-doing flag.")
        sys.exit(1)

    # Rate limiting setup
    sleep_time = 0
    if args.rate > 0:
        sleep_time = 3600 / args.rate  # Seconds per email

    # Prepare outbox.csv header
    write_outbox_csv({"timestamp": "", "email": "", "subject": "", "status": "", "error_message": ""}, mode='w')

    sent_count = 0
    failed_count = 0
    if args.dry_run:
        Path("previews").mkdir(exist_ok=True)

    for idx, row_series in tqdm(contacts_df.iterrows(), total=len(contacts_df), desc="Processing Emails"):
        contact = row_series.to_dict()
        recipient_email = contact.get("email")

        if not recipient_email or not re.match(r"[^@]+@[^@]+\.[^@]+", recipient_email):
            logger.warning(f"Skipping invalid or missing email in row {idx + args.start}: {recipient_email}")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email or "N/A",
                "subject": subject_template.render(contact),
                "status": "skipped",
                "error_message": "Invalid or missing email address"
            })
            failed_count += 1
            continue
        
        # Prepare sender details
        sender_email = args.sender_name_email
        if not sender_email: # Fallback to authenticated user's email if --from not provided
            try:
                profile = service.users().getProfile(userId='me').execute()
                sender_email = profile['emailAddress']
                logger.info(f"Using authenticated user's email as sender: {sender_email}")
            except Exception as e:
                logger.error(f"Could not retrieve authenticated user's email for sender: {e}. Please provide --from argument.")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": recipient_email,
                    "subject": subject_template.render(contact),
                    "status": "failed_sender_config",
                    "error_message": str(e)
                })
                failed_count += 1
                continue

        try:
            # Render subject and body
            final_subject = subject_template.render(contact)
            rendered_html = html_template.render(contact, sender_name=args.sender_name_email.split(" <")[0].strip() if "<" in args.sender_name_email else args.sender_name_email)
            plain_text_content = strip_html_tags(rendered_html)

            message_body = create_message(
                sender_email, recipient_email, final_subject,
                rendered_html, plain_text_content
            )

            if args.dry_run:
                preview_file = Path("previews") / f"email_preview_{idx + args.start}.eml"
                with open(preview_file, "w") as f:
                    # Create a dummy message for preview
                    msg = MIMEMultipart("alternative")
                    msg["From"] = sender_email
                    msg["To"] = recipient_email
                    msg["Subject"] = final_subject
                    msg.attach(MIMEText(plain_text_content, "plain"))
                    msg.attach(MIMEText(rendered_html, "html"))
                    f.write(msg.as_string())
                logger.info(f"[DRY RUN] Saved email preview for {recipient_email} to {preview_file}")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": recipient_email,
                    "subject": final_subject,
                    "status": "preview_saved",
                    "error_message": ""
                })
            elif args.test_to:
                test_recipient = args.test_to
                logger.info(f"Sending test email to {test_recipient} for contact from row {idx + args.start}...")
                test_message_body = create_message(
                    sender_email, test_recipient, final_subject,
                    rendered_html, plain_text_content
                )
                send_gmail_api_message(service, "me", test_message_body)
                logger.info(f"Successfully sent test email to {test_recipient}.")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": test_recipient,
                    "subject": final_subject,
                    "status": "test_sent",
                    "error_message": ""
                })
                sys.exit(0) # Exit after sending one test email
            else:
                logger.info(f"Sending email to {recipient_email} (Row {idx + args.start})...")
                send_gmail_api_message(service, "me", message_body)
                logger.info(f"Successfully sent email to {recipient_email}.")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": recipient_email,
                    "subject": final_subject,
                    "status": "sent",
                    "error_message": ""
                })
                sent_count += 1

        except HttpError as e:
            status_code = e.resp.status
            error_msg = f"Gmail API Error ({status_code}): {e}"
            logger.error(f"{error_msg} sending to {recipient_email} (Row {idx + args.start})")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email,
                "subject": final_subject,
                "status": f"failed_api_{status_code}",
                "error_message": error_msg
            })
            failed_count += 1
        except Exception as e:
            logger.error(f"General Error processing {recipient_email} (Row {idx + args.start}): {e}")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email,
                "subject": final_subject,
                "status": "failed_general",
                "error_message": str(e)
            })
            failed_count += 1
        finally:
            if sleep_time > 0 and not (args.dry_run or args.test_to):
                logger.debug(f"Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)

    logger.info(f"Email sending process completed. Sent: {sent_count}, Failed: {failed_count}")


if __name__ == "__main__":
    main()
