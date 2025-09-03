import imaplib
import email
from .config import GMAIL_USERNAME, GMAIL_PASSWORD, IMAP_SERVER, SUBJECT_FILTER

# Search for unread emails where the subject starts with '[Amplitude] Taxonomy Validation Errors for'
def get_unread_emails():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    mail.select("inbox")

    # Search for unread emails where the subject starts with '[Amplitude] Taxonomy Validation Errors for'
    search_criteria = f'(UNSEEN SUBJECT "{SUBJECT_FILTER}")'
    result, data = mail.search(None, search_criteria)

    email_ids = data[0].split()
    emails_content = []

    for email_id in email_ids:
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    email_content = part.get_payload(decode=True).decode()
                    emails_content.append((email_id, email_content))
                    break
        else:
            email_content = msg.get_payload(decode=True).decode()
            emails_content.append((email_id, email_content))

    return mail, email_ids, emails_content

# Mark emails as read
def mark_emails_as_read(mail, email_ids):
    for email_id in email_ids:
        mail.store(email_id, "+FLAGS", "\\Seen")
    mail.logout()
