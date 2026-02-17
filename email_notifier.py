import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import html

load_dotenv()

SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(new_items):
    if not new_items:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🖼️ New Postcards Found: {len(new_items)}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    rows = []
    for item in new_items:
        title = html.escape(item.get("title", ""))
        url = item.get("url", "")
        price = item.get("price")
        ship = item.get("shipping")

        price_str = f"${price:.2f}" if isinstance(price, (int, float)) else "N/A"
        ship_str = f"${ship:.2f}" if isinstance(ship, (int, float)) else "N/A"

        rows.append(f"""
          <li>
            <a href="{url}" target="_blank">{title}</a><br>
            Price: {price_str} &nbsp; Shipping to Palmer: {ship_str}
          </li>
        """)

    html_body = f"""
    <html>
      <body>
        <h2>New eBay Postcards</h2>
        <ul>
          {''.join(rows)}
        </ul>
      </body>
    </html>
    """

    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
