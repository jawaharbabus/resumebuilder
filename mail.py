import smtplib
from email.message import EmailMessage
import mimetypes
import os
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Config ---
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")

# --- Create Email ---
class Mailer:
    def sender_email(receiver_email,attachment_path,subject,body):
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)

        # --- Add Attachment ---
        if os.path.exists(attachment_path):
            mime_type, _ = mimetypes.guess_type(attachment_path)
            mime_type = mime_type or "application/octet-stream"
            maintype, subtype = mime_type.split("/", 1)

            with open(attachment_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
        else:
            print(f"Attachment not found: {attachment_path}")
            exit(1)

        # --- Send Email ---
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("Email sent successfully!")


