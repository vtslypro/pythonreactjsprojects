__author__ = 'alonitzhaki'
import imaplib
import email


class GmailClient(object):
    host = 'imap.gmail.com'
    label_open = None
    label_open_status = False

    def __init__(self):
        self.mail_client = imaplib.IMAP4_SSL(GmailClient.host)

    def connect_to_account(self, address, password):
        self.mail_client = imaplib.IMAP4_SSL(GmailClient.host)
        try:
            self.mail_client.login(user=address, password=password)
        except imaplib.IMAP4.error as e:
            print(
            'GmailClient.connect_to_account: Exception while trying to login to: ' + address + '. Exception msg: ' + str(
                e.message) + '. Exception args: ' + str(e.args) + '\n')
            raise 'Failed connecting to account: ' + address + '. Exception message: ' + str(e.message) + \
                  '. Exception args: ' + str(e.args)

    def close_and_logout(self):
        if self.label_open_status is True:
            self.mail_client.close()
        self.mail_client.logout()

    def get_labels(self):
        return_value, labels = self.mail_client.list()
        if return_value == 'OK':
            return labels
        return None

    def open_label(self, label_name):
        return_value, data = self.mail_client.select(mailbox=label_name, readonly=True)
        if return_value == 'OK':
            self.label_open = label_name
            self.label_open_status = True
            return True
        return False

    def search_mails_in_label(self, subject_to_search):
        return_value, message_numbers = self.mail_client.search(None, 'ALL')
        if return_value == 'OK':

            for num in message_numbers[0].split():
                return_value, raw_data = self.mail_client.fetch(message_set=num, message_parts='(RFC822)')

                if return_value == 'OK':
                    message = email.message_from_string(raw_data[0][1])
                    message_subject = message['Subject']

                    if subject_to_search == message_subject:
                        return message_subject, message['From'], message['To'], message['Date']
        return None
