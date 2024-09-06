import imaplib
import sys
import os
import email
from email.header import decode_header
from dotenv import load_dotenv

# Handles everything related to IMAP
class IMAPClient:
    def __init__(self):
        load_dotenv()
        self.total_number_of_emails = None
        self.number_of_unread_emails = 3
        self.server = os.getenv('SERVER')
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap = imaplib.IMAP4_SSL(self.server)

    def authentication(self):
        """
        Authenticate with IMAP server
        :param self:
        """

        try:
            self.imap.login(self.username, self.password)
            print(f"Authentication successful for {self.username}")
        except imaplib.IMAP4.error:
            print("Authentication failed")
            sys.exit(1)

    def select_inbox(self):
        """
        Select the INBOX folder on the IMAP server.
        Raises:
            Exception: If selecting the INBOX folder fails.
        Return: total_number_of_emails (int): The total number of inbox emails.
        """
        # self.imap.select =
        # returns a tuple of status response (string)
        # and the number of emails in the inbox (string)
        status, total_number_of_emails = self.imap.select("INBOX")
        # total_number_of_emails = int(total_number_of_emails) #[b'3]
        if status != "OK":
            raise Exception("Failed to select INBOX")
        else:
            print("Selected INBOX")
        total_number_of_emails = int(total_number_of_emails[0]) # convert byte representation to int
        self.total_number_of_emails = total_number_of_emails


    def fetch_emails(self):
        """
           Fetch a specified number of emails from the selected mailbox.

           Raises:
               Exception: If fetching emails fails.
           """
        from_email_sender = None
        print("Starting to fetch emails...\n")

        for i in range(self.total_number_of_emails, self.total_number_of_emails - self.number_of_unread_emails, -1):
            if i <= 0:
                break  # Ensure we don't fetch invalid message IDs

            # fetch the email message by ID
            fetch_status, email_message = self.imap.fetch(str(i), "(RFC822)")
            for response in email_message:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    email_message = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = decode_header(email_message["Subject"])[0]

                    # check if the from_email_sender variable is the instance of bytes type
                    if isinstance(from_email_sender, bytes):
                        from_email_sender = from_email_sender.decode(encoding if encoding else 'utf-8')

                    print("Subject:", subject)
                    print("From:", from_email_sender)

                    if email_message.is_multipart():
                        self.email_is_multipart(email_message)

                    else:
                        self.email_is_single_part(email_message)

    def email_is_multipart(self, email_message):
        """
        helper function for fetch_emails()
        helps with multipart emails
        :return:
        """
        body = None
        # if the email message is multipart, containing multiple parts.
        # the loop will process each individual part
        # iterate over email parts
        for part in email_message.walk():
            # extract content type of email
            content_type = part.get_content_type()

            # indicates how the part should be handled("attachment", "inline")
            content_disposition = str(part.get('Content-Disposition'))

            # get the email body
            try:
                # extracts the payload and puts it into t
                body = part.get_payload(decode=True).decode()
            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                # print text/plain emails and skip attachments
                print(body)

            elif "attachment" in content_disposition:
                print("there is an attachment in here")
                print("potential plan to post attachment into JIRA ticket?")

    def email_is_single_part(self, email_message):
        """
        helper function for fetch_emails()
        helps with single part emails
        :return:
        """
        # extract content type of email
        content_type = email_message.get_content_type()
        # get the email body
        body = email_message.get_payload(decode=True).decode()
        if content_type == "text/plain":
            # print only text email parts
            print(body)

        if content_type == "text/html":
            print("This file contains HTML content.")
            print("What do with this sort of email?")

    def close_imap(self):
        self.imap.close()
        self.imap.logout()


