""" libraries: smtplib, ssl"""

import smtplib
from email.message import EmailMessage
from datetime import datetime
from decouple import config

def send_email(message):
    port = 465  # used for  ssl
    smtp_server = "smtp.gmail.com"

    sender_email = config('EMAIL_ADDRESS')
    password = config('PASSWORD')

    receiver_emails =  ['tankhanhf7@gmail.com']
    msg = EmailMessage()
    msg.set_content(message)
    msg['From'] = sender_email
    msg['To'] = receiver_emails
    msg['Subject'] = f"Prices Tracking on {datetime.today().strftime('%m-%d-%Y')}"

    
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        try: 
            server.login(sender_email, password)
            server.send_message(msg)
            print("Sent Successfully!!!")
        except:
            print("Failed!!!")


if __name__ == '__main__':
    send_email('Hello World')


    # 'tranthanhtinchristian99@gmail.com', 'tan.dao@sjsu.edu'