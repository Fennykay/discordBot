#file will send text to given phone number using smtplib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

KNOWN_EMAILS = {
    "kenny": "fancherk@outlook.com",
    "ky": "kyleefdarling@yahoo.com"
}

EMAIL = "text19910405@gmail.com"
PASSWORD = "TextingPassword!"
APP_PASSWORD = "vcko kgwp qsoh csas"

def send_message(email, message):
    auth = (EMAIL, APP_PASSWORD)
    if email in KNOWN_EMAILS:
        email = KNOWN_EMAILS[email]

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = email
        msg['Subject'] = "Message from Python"
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, email, text)
        server.quit()
        print(f"Message sent to {email}")

    except smtplib.SMTPException as e:
        print(f"Failed to send message to {email}: {e}")

if __name__ == "__main__":
    #get inputs
    email = input("Enter email or name: ")
    message = input("Enter message: ")

    send_message(email, message)