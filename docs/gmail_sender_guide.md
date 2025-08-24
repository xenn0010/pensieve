# Gmail API Email Sender

A reliable command-line tool to send personalized HTML emails from a CSV file using the Gmail API via OAuth 2.0. This tool ensures secure authentication, flexible templating, rate-limiting, and comprehensive logging.

## ✨ Features

-   **Secure OAuth 2.0 Authentication**: Uses Google's official SDKs to authenticate with the Gmail API via OAuth, storing refresh tokens securely.
-   **CSV Input**: Reads recipient data from a CSV file, supporting custom fields for dynamic content.
-   **Jinja2 Templating**: Renders dynamic HTML email content, including the subject line, with per-row variables.
-   **HTML + Plain-Text**: Automatically generates a plain-text fallback version from your HTML template for better email compatibility.
-   **Gmail API (messages.send)**: Sends emails directly via the robust Gmail API.
-   **Rate Limiting**: Prevents overwhelming Gmail servers with configurable send rates.
-   **Retry Mechanism**: Automatically retries sending failed emails (specifically for 429/5xx HTTP errors) with exponential backoff.
-   **Comprehensive Logging**: Records all email sending attempts (successes, failures, skips) to `outbox.log` (detailed) and `outbox.csv` (summary).
-   **Dry Run Mode (`--dry-run`)**: Renders emails and saves them as `.eml` preview files in `./previews/` without actually calling the Gmail API.
-   **Test Mode (`--test-to`)**: Renders the first valid row's email and sends it as a single test email to a specified address, then exits.
-   **Chunking (`--start`, `--end`)**: Supports sending to a subset of contacts within a a specified row range.
-   **Safety Checks**: Requires explicit confirmation (`--i-know-what-im-doing`) for sending to more than 100 recipients in one run.

## 🚀 Quick Start

### 1. Google Cloud Project Setup

To use the Gmail API, you need to set up a project in Google Cloud Console and enable the Gmail API. Follow these steps:

1.  **Go to Google Cloud Console**: Navigate to [console.cloud.google.com](https://console.cloud.google.com/).
2.  **Create a New Project**: If you don't have one, create a new project.
3.  **Enable Gmail API**: Search for "Gmail API" in the API & Services library and enable it.
4.  **Create OAuth Consent Screen**: 
    *   Go to `APIs & Services > OAuth consent screen`.
    *   Configure the consent screen with your application's details (e.g., app name, support email, developer contact information).
    *   For `User type`, select `External` and `Publishing status` to `Testing` or `In production`.
    *   Add the `https://www.googleapis.com/auth/gmail.send` scope.
    *   Add your email address as a `Test user` if your publishing status is `Testing`.
5.  **Create Credentials**: 
    *   Go to `APIs & Services > Credentials`.
    *   Click `+ CREATE CREDENTIALS` and select `OAuth client ID`.
    *   For `Application type`, choose `Desktop app`.
    *   Give it a name (e.g., "Gmail Sender CLI").
    *   Click `CREATE`.
6.  **Download `credentials.json`**: A dialog will appear with your client ID and client secret. Click `DOWNLOAD JSON` to save your `credentials.json` file. **Place this file in the root directory of this project.**

### 2. Local Environment Setup

1.  **Clone the Repository (if not already done)**:

    ```bash
    git clone <your-repo-url>
    cd gmail-api-sender
    ```

2.  **Create a Virtual Environment and Install Dependencies**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Create `.env` Configuration File**:

    Rename `.env.example` to `.env` in the project root and customize it:

    ```ini
    FROM_NAME="Your Name"
    # Optional: Override rate limit (emails per hour)
    # RATE=120
    # Optional: Override subject line (Jinja2 templated)
    # SUBJECT="Custom Subject {{ first_name }}"
    ```

    -   `FROM_NAME`: The name to appear as the sender (e.g., "Your Company"). This can be overridden by the `--from` CLI argument.
    -   `RATE`: Optional. Override the default rate limit of 60 emails/hour. 
    -   `SUBJECT`: Optional. Override the default subject line. This field supports Jinja2 templating.

### 3. Prepare Contacts CSV

Create a `contacts.csv` file with your recipient list. The first row must be headers. A `email` column is required, and other columns can be used for template variables.

```csv
email,first_name,company,plan
alice@example.com,Alice,Acme,Pro
bob@example.com,Bob,Zenith,Basic
charlie@example.com,Charlie,Globex,Enterprise
```

### 4. Design HTML Template

Create a `template.html` file with Jinja2-style placeholders. These placeholders will be replaced by data from your `contacts.csv`.

```html
<!doctype html>
<html>
  <body>
    <p>Hi {{ first_name }},</p>
    <p>Quick note about your {{ plan }} plan at {{ company }}.</p>
    <p>We’ve added new features—reply if you’d like a 10-minute walkthrough.</p>
    <p>Cheers,<br>{{ sender_name }}</p>
  </body>
</html>
```

Missing fields in the CSV will gracefully fall back to an empty string (or the `default` filter's value if used in the template).

## ⚙️ Usage

Run the `gmail_send.py` script from your terminal:

```bash
python3 gmail_send.py --help
```

### First-time OAuth Authorization

The first time you run `gmail_send.py`, it will open a browser window for you to authorize access to your Gmail account. Follow the prompts to grant the necessary permissions. After successful authorization, a `token.json` file will be created in your project root, which will be used for subsequent authentications.

### Common Commands

**Send emails to all contacts (requires safety flag for >100 emails):**

```bash
python3 gmail_send.py \
  --csv contacts.csv \
  --template template.html \
  --subject "Special Offer for {{ first_name }}!" \
  --from "Your Company Name <your_email@gmail.com>" \
  --rate 60 \
  --i-know-what-im-doing # Only if sending to >100 recipients
```

**Perform a dry run (saves .eml files to `./previews/`):**

```bash
python3 gmail_send.py \
  --csv contacts.csv \
  --template template.html \
  --subject "Dry Run Subject" \
  --from "Test Sender <test@example.com>" \
  --dry-run
```

**Send a single test email:**

```bash
python3 gmail_send.py \
  --csv contacts.csv \
  --template template.html \
  --subject "Test Email" \
  --from "Test Sender <test@example.com>" \
  --test-to your_personal_email@example.com
```

**Send emails to a specific range of contacts:**

```bash
python3 gmail_send.py \
  --csv contacts.csv \
  --template template.html \
  --subject "Batch Send Update" \
  --from "Batch Sender <batch@example.com>" \
  --start 2 \
  --end 5
```

## CLI Arguments

-   `--csv FILE`: Path to the contacts CSV file (default: `contacts.csv`).
-   `--template FILE`: Path to the HTML email template (default: `template.html`).
-   `--subject TEXT`: Subject line of the email. This field supports Jinja2 templating (required).
-   `--from "Name <email@domain.com>"`: Sender name and email address. If not provided, it defaults to the authenticated Gmail user's email. If only a name is provided (e.g., "Helen"), it will use "Helen <authenticated_user@gmail.com>".
-   `--rate N`: Emails per hour for rate limiting (default: `60`).
-   `--dry-run`: Render emails and save as `.eml` files in `./previews/` without sending.
-   `--retries N`: Maximum retries for sending failed emails (default: `3`). Uses exponential backoff for `429`, `500`, `502`, `503`, `504` HTTP errors. Other `4xx` errors are considered permanent failures.
-   `--start N`: Starting row in the CSV (1-indexed, inclusive, default: `1`).
-   `--end N`: Ending row in the CSV (1-indexed, inclusive).
-   `--test-to EMAIL`: Render the first valid row's email and send one test email to this address, then exit.
-   `--i-know-what-im-doing`: **Required** to send more than 100 emails in one run. Use with extreme caution!

## 📝 Logging and Tracking

-   `outbox.log`: A rolling file log for detailed operational messages, including OAuth flow, API calls, errors, and debug information.
-   `outbox.csv`: Records a summary of each email attempt:
    -   `timestamp`: When the attempt occurred.
    -   `email`: Recipient's email address.
    -   `subject`: Email subject.
    -   `status`: `sent`, `failed_api_XXX` (e.g., `failed_api_400`), `failed_general`, `skipped`, `preview_saved`, `test_sent`, `failed_sender_config`.
    -   `error_message`: Details of any error that occurred.

## ⚠️ Troubleshooting

-   **`credentials.json` Not Found**: Ensure you have downloaded `credentials.json` from your Google Cloud Project and placed it in the project root.
-   **OAuth Flow Issues**: If the browser doesn't open or authorization fails, check your network, browser settings, and ensure the `redirect_uri` for `Desktop app` in Google Cloud Console is correctly configured (usually `http://localhost:<some_port>`). The script uses `port=0` to find an available port.
-   **Gmail API Errors**: Check `outbox.log` for specific `HttpError` details. Common issues include API rate limits (which the script retries for), invalid recipients, or insufficient permissions (check your OAuth scopes).
-   **Invalid Email Addresses in CSV**: These will be skipped and logged to `outbox.log` and `outbox.csv`.
-   **Template Rendering Errors**: Ensure Jinja2 placeholders in `template.html` and the `--subject` argument match your CSV headers.
-   **`FROM_NAME`/`--from` Issues**: If you don't provide `--from` and the script can't determine your authenticated Gmail user's email, it will log an error. Ensure the authenticated user has an email address.
-   **Rate Limit Exceeded (beyond retries)**: If you consistently hit 429 errors, consider reducing the `--rate` or requesting a higher quota in Google Cloud.

## 🤝 Contribution

Feel free to fork, modify, and contribute to this project. Pull requests are welcome!
