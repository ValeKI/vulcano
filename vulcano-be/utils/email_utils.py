import smtplib
from email.mime.text import MIMEText
from config import CURRENT_CONFIG

class EmailUtils:
    def send_reset_email(self, to_email, reset_link):
        print("SMTP_USER:", CURRENT_CONFIG.SMTP_USER)
        msg = MIMEText(f"Clicca qui per resettare la tua password: {reset_link}")
        msg["Subject"] = "Recupero Password"
        msg["From"] = CURRENT_CONFIG.SMTP_USER or "noreply@example.com"
        msg["To"] = to_email

        with smtplib.SMTP(CURRENT_CONFIG.SMTP_HOST, CURRENT_CONFIG.SMTP_PORT) as server:
            server.sendmail(msg["From"], [to_email], msg.as_string())
        print("Email inviata!")