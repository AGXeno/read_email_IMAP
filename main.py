from IMAPClient import IMAPClient


def Start_IMAP():
    print("Starting script...")
    try:
        imap = IMAPClient()
    except Exception as e:
        print(f"Error starting up IMAP: {e}")
        exit(1)
    print("Connecting to IMAP server...")
    imap.authentication()
    imap.select_inbox()
    imap.fetch_emails()
    imap.close_imap()

def main():
    Start_IMAP()


if __name__ == '__main__':
    main()
