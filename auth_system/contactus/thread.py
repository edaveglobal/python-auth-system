
import threading
import logging
from datetime import datetime
from smtplib import SMTPException


from .send_email import send_customer_message

class SendCustomerContactUsMessage(threading.Thread):
    
    def __init__(self , subject, email_from , message, username):
        self._email = email_from
        self._subject = subject
        self._message = message
        self._username = username
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            send_customer_message(email_from=self._email, message=self._message, subject=self._subject, username=self._username)
            logging.info(f"Customer contact us message delivered around {datetime.now()}")
        except SMTPException as e:
            logging.debug('There was an error sending the customer message. '+ e)
        
       