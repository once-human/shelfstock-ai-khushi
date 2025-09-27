import streamlit as st
import smtplib
from email.mime.text import MIMEText
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configs

# --- Email Configuration (Fetch from configs or secrets) ---
# IMPORTANT: Use st.secrets or environment variables in a real app!
# Example using placeholders from configs.py (replace with your actual source)
SMTP_SERVER = getattr(configs, "SMTP_SERVER", None)
SMTP_PORT = getattr(configs, "SMTP_PORT", 587) # Default TLS port
SMTP_USERNAME = getattr(configs, "SMTP_USERNAME", None)
SMTP_PASSWORD = getattr(configs, "SMTP_PASSWORD", None) # Use App Password if 2FA enabled
SENDER_EMAIL = getattr(configs, "SENDER_EMAIL", None)

def send_email(recipient_email: str, subject: str, body: str) -> bool:
    """Sends an email using SMTP configuration."""
    
    # Check if configuration is complete
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, recipient_email]):
        missing = [
            name for name, value in 
            [("SMTP_SERVER", SMTP_SERVER), ("SMTP_PORT", SMTP_PORT), 
             ("SMTP_USERNAME", SMTP_USERNAME), ("SMTP_PASSWORD", SMTP_PASSWORD), 
             ("SENDER_EMAIL", SENDER_EMAIL), ("recipient_email", recipient_email)] 
            if not value
        ]
        st.error(f"Email configuration incomplete. Missing: {', '.join(missing)}. Cannot send email.")
        # In a real app, you might log this error instead of showing to user
        print(f"[Email Error] Configuration incomplete. Missing: {', '.join(missing)}")
        return False

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        st.spinner(f"Connecting to email server {SMTP_SERVER}...")
        # Connect to SMTP server (TLS)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [recipient_email], msg.as_string())
            print(f"Email sent successfully to {recipient_email}")
            return True
    except smtplib.SMTPAuthenticationError as e:
        st.error("Email Login Failed: Check username/password (or use App Password if 2FA is enabled).", icon="🚨")
        print(f"[Email Error] SMTP Authentication Error: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        st.error(f"Email Connection Failed: Could not connect to {SMTP_SERVER}:{SMTP_PORT}.", icon="🚨")
        print(f"[Email Error] SMTP Connect Error: {e}")
        return False
    except smtplib.SMTPSenderRefused as e:
         st.error(f"Email Sending Failed: Sender address {SENDER_EMAIL} might be refused.", icon="🚨")
         print(f"[Email Error] SMTP Sender Refused: {e}")
         return False
    except Exception as e:
        st.error(f"An unexpected error occurred while sending email: {e}", icon="🚨")
        print(f"[Email Error] Unexpected Error: {e}")
        return False 