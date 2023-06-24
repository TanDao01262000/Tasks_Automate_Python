import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import chardet
# from summarize_api import summarize_content
from reformat_content import clean_string


def fetch():
    content_list = list()

    # Load info and login
    load_dotenv()
    IMAP_SERVER = 'imap.gmail.com'
    USERNAME = 'tankhanhdao@gmail.com'
    PASSWORD = os.getenv('PASSWORD')
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)

    # Fetch the emails in the INBOX list
    mailbox = 'INBOX'
    status, response = imap.select(mailbox)
    if status != 'OK':
        print(f"Failed to select mailbox '{mailbox}'")
        imap.logout()
        exit(1)

    # Search for emails within the last 12 hours
    date_limit = datetime.now() - timedelta(hours=12)
    date_limit_str = date_limit.strftime('%d-%b-%Y')
    search_criteria = f'SINCE "{date_limit_str}"'
    status, response = imap.search(None, search_criteria)
    if status != 'OK':
        print("Failed to fetch email IDs")
        imap.logout()
        exit(1)

    email_ids = response[0].split()
    for email_id in email_ids:
        status, response = imap.fetch(email_id, '(RFC822)')
        if status != 'OK':
            print(f"Failed to fetch email with ID: {email_id}")
            continue
        raw_email = response[0][1]
        parsed_email = email.message_from_bytes(raw_email)

        # Get email subject
        subject = decode_header(parsed_email['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

        # Get email sender's address
        sender = decode_header(parsed_email['From'])[0][0]
        if isinstance(sender, bytes):
            sender = sender.decode()

        # Get email sent time
        date_time = parsed_email['Date']
        if date_time is None:
            date_time = 'N/A'

        # Get email content
        content = ''
        if parsed_email.is_multipart():
            for part in parsed_email.walk():
                if part.get_content_type() == "text/plain":
                    content_bytes = part.get_payload(decode=True)
                    encoding = chardet.detect(content_bytes)['encoding']
                    content = content_bytes.decode(encoding, errors='ignore')
                    break
        else:
            content_bytes = parsed_email.get_payload(decode=True)
            encoding = chardet.detect(content_bytes)['encoding']
            content = content_bytes.decode(encoding, errors='ignore')

        # Fetch about 10 characters from the content
        content = content if content else 'N/A'

        content_obj = dict()
        content_obj['sender'] = sender
        content_obj['subject'] = subject
        content_obj['time'] = date_time
        content_obj['content'] = content[:100]  # only get 100 characters from the content
        content_list.append(content_obj)

    imap.logout()
    return content_list


if __name__ == '__main__':
    content = fetch()
    print('Content:',clean_string(content[0]['content']) )
