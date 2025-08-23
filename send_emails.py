#!/usr/bin/env python3

import argparse
import csv
import email
import logging
import os
import re
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from tenacity import (retry, stop_after_attempt, wait_exponential, 
                       retry_if_exception_type)

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

# Load environment variables
load_dotenv()

# Email validation regex (simple but effective for basic validation)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


# --- Helper Functions ---

def strip_html_tags(html_content: str) -> str:
    """Strips HTML tags to create a plain-text version of the email."""
    # A very basic HTML stripping. For robust stripping, consider BeautifulSoup.
    text = re.sub(r'<[^>]+>', '', html_content)
    return text.strip()


def write_outbox_csv(data: dict, mode: str = 'a'):
    """Writes email sending results to outbox.csv."""
    file_exists = os.path.isfile("outbox.csv")
    with open("outbox.csv", mode, newline='') as f:
        fieldnames = ["timestamp", "email", "subject", "status", "error_message"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or mode == 'w':
            writer.writeheader()
        writer.writerow(data)


def validate_email(email_address: str) -> bool:
    """Validates an email address using a regex."""
    return bool(EMAIL_REGEX.match(email_address))


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10),
       retry=retry_if_exception_type(smtplib.SMTPTransientError))
def send_email_smtp(
    sender_email: str,
    recipient_email: str,
    subject: str,
    html_content: str,
    plain_text_content: str,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    smtp_use_tls: bool
) -> None:
    """Sends a single email via SMTP with retry logic."""
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(plain_text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if smtp_use_tls:
            server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


# --- Main Logic ---

def main():
    parser = argparse.ArgumentParser(description="Auto-Email Sender CLI")
    parser.add_argument("--csv", default="contacts.csv", help="Path to the contacts CSV file.")
    parser.add_argument("--template", default="template.html", help="Path to the HTML email template.")
    parser.add_argument("--subject", required=True, help="Subject of the email.")
    parser.add_argument("--from", dest="sender_email", required=True, help="Sender email address (e.g., 'Name <sender@domain.com>').")
    parser.add_argument("--rate", type=int, default=60, help="Emails per hour for rate limiting.")
    parser.add_argument("--dry-run", action="store_true", help="Render emails and save as .eml files, but do not send.")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries for sending failed emails.")
    parser.add_argument("--start-row", type=int, default=1, help="Starting row in the CSV (1-indexed).")
    parser.add_argument("--end-row", type=int, help="Ending row in the CSV (inclusive, 1-indexed).")
    parser.add_argument("--test-to", help="Send one test email to this address for the first valid row, then exit.")
    parser.add_argument("--i-know-what-im-doing", action="store_true",
                        help="Required to send more than 100 emails in one run.")

    args = parser.parse_args()

    # Load SMTP settings from .env
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

    if not all([smtp_host, smtp_user, smtp_pass]):
        logger.error("Missing SMTP credentials in .env. Please check SMTP_HOST, SMTP_USER, SMTP_PASS.")
        sys.exit(1)

    # Set up Jinja2 environment
    template_dir = os.path.dirname(args.template) if os.path.dirname(args.template) else "."
    template_name = os.path.basename(args.template)
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"])
    )
    try:
        template = env.get_template(template_name)
    except Exception as e:
        logger.error(f"Error loading template {args.template}: {e}")
        sys.exit(1)

    # Rate limiting setup
    sleep_time = 0
    if args.rate > 0:
        sleep_time = 3600 / args.rate  # Seconds per email

    contacts_to_process = []
    try:
        with open(args.csv, 'r') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                if args.start_row <= i and (args.end_row is None or i <= args.end_row):
                    contacts_to_process.append(row)
    except FileNotFoundError:
        logger.error(f"Contacts CSV file not found: {args.csv}")
        sys.exit(1)

    if not contacts_to_process:
        logger.info("No contacts to process in the specified range.")
        sys.exit(0)

    # Safety check for large sends
    if len(contacts_to_process) > 100 and not args.i_know_what_im_doing:
        logger.error("Sending to more than 100 recipients requires --i-know-what-im-doing flag.")
        sys.exit(1)

    # Process contacts
    sent_count = 0
    failed_count = 0
    if args.dry_run:
        os.makedirs("previews", exist_ok=True)

    for i, contact in enumerate(contacts_to_process, args.start_row):
        recipient_email = contact.get("email")

        if not recipient_email or not validate_email(recipient_email):
            logger.warning(f"Skipping invalid or missing email in row {i}: {recipient_email}")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email or "N/A",
                "subject": args.subject,
                "status": "skipped",
                "error_message": "Invalid or missing email address"
            })
            failed_count += 1
            continue

        try:
            # Render HTML content, providing default empty string for missing fields
            rendered_html = template.render(contact)
            plain_text_content = strip_html_tags(rendered_html)

            if args.dry_run:
                preview_file = os.path.join("previews", f"email_preview_{i}.eml")
                with open(preview_file, "w") as f:
                    # Create a dummy message for preview
                    msg = MIMEMultipart("alternative")
                    msg["From"] = args.sender_email
                    msg["To"] = recipient_email
                    msg["Subject"] = args.subject
                    msg.attach(MIMEText(plain_text_content, "plain"))
                    msg.attach(MIMEText(rendered_html, "html"))
                    f.write(msg.as_string())
                logger.info(f"[DRY RUN] Saved email preview for {recipient_email} to {preview_file}")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": recipient_email,
                    "subject": args.subject,
                    "status": "preview_saved",
                    "error_message": ""
                })
            elif args.test_to:
                test_recipient = args.test_to
                logger.info(f"Sending test email to {test_recipient} for contact from row {i}...")
                send_email_smtp(
                    args.sender_email, test_recipient, args.subject, 
                    rendered_html, plain_text_content,
                    smtp_host, smtp_port, smtp_user, smtp_pass, smtp_use_tls
                )
                logger.info(f"Successfully sent test email to {test_recipient}.")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": test_recipient,
                    "subject": args.subject,
                    "status": "test_sent",
                    "error_message": ""
                })
                sys.exit(0) # Exit after sending one test email
            else:
                logger.info(f"Sending email to {recipient_email} (Row {i})...")
                send_email_smtp(
                    args.sender_email, recipient_email, args.subject, 
                    rendered_html, plain_text_content,
                    smtp_host, smtp_port, smtp_user, smtp_pass, smtp_use_tls
                )
                logger.info(f"Successfully sent email to {recipient_email}.")
                write_outbox_csv({
                    "timestamp": datetime.now().isoformat(),
                    "email": recipient_email,
                    "subject": args.subject,
                    "status": "sent",
                    "error_message": ""
                })
                sent_count += 1

        except smtplib.SMTPException as e:
            logger.error(f"SMTP Error sending to {recipient_email} (Row {i}): {e}")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email,
                "subject": args.subject,
                "status": "failed_smtp",
                "error_message": str(e)
            })
            failed_count += 1
        except Exception as e:
            logger.error(f"General Error processing {recipient_email} (Row {i}): {e}")
            write_outbox_csv({
                "timestamp": datetime.now().isoformat(),
                "email": recipient_email,
                "subject": args.subject,
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
