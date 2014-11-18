from time import time
from smtplib import SMTP, SMTPException
from email.MIMEText import MIMEText

from locust import Locust, events

import sys


class SmtpClient(object):
    """
        This class acts as a wrapper around the native smtplib.SMTP class.  Simply logs time before
        passing the message upstream and registers the appropriate locust events.
    """

    obj = None

    def __init__(self, *args, **kwargs):
        self.obj = SMTP(*args, **kwargs)

    def __getattr__(self, item):
        func = getattr(self.obj, item)

        def wrapper(*args, **kwargs):
            start_time = time()

            try:
                result = func(*args, **kwargs)
            except SMTPException as e:
                exc_time = int((time() - start_time) * 1000)

                # register failure event
                events.request_failure.fire(
                    request_type='smtp',
                    name=item,
                    response_time=exc_time,
                    exception=e)
            else:
                exc_time = int((time() - start_time) * 1000)

                # register success event
                events.request_success.fire(
                    request_type='smtp',
                    name=item,
                    response_time=exc_time,
                    response_length=0)

            return result
        return wrapper


class SmtpLocust(Locust):
    """
    Abstract Locust test class for subclassing.  It provides an SMTP client.
    """

    host = None
    port = 25
    client = None

    username = None
    password = None

    debug = False

    # Locust attributes
    min_wait = 1
    max_wait = 1

    def __init__(self, *args, **kwargs):
        super(SmtpLocust, self).__init__(*args, **kwargs)

        self.client = SmtpClient(self.host, self.port)

        # don't want to trigger wrapper getattr
        self.client.obj.set_debuglevel(self.debug)

        if self.username is not None and self.password is not None:
            self.client.login(self.username, self.password)
