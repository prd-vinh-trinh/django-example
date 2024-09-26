import threading

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class MailingThread(threading.Thread):
    def __init__(
        self,
        messages=None,
        fail_callback=None
    ):
        self.messages = messages
        self.fail_callback = fail_callback
        threading.Thread.__init__(self)

    def run(self):
        for message in self.messages:
            try:
                message.send()
            except Exception as e:
                print(str(e))
                if self.fail_callback:
                    self.fail_callback(message)


class Mailing:
    @staticmethod
    def asyn_send_messages(messages):
        MailingThread(messages=messages).start()

    @staticmethod
    def asyn_send_message(message):
        MailingThread(messages=[message]).start()

    @classmethod
    def create_html_message(cls, data, attachment=None, headers=None):
        subject = data.get("subject")
        from_email = data.get(
            "from") or settings.DEFAULT_FROM_EMAIL or "Django-example <noreply@domain.com.vn>"
        to = data.get("to")
        html_content = render_to_string(
            data.get("template"), data.get("context")
        )

        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, to, headers
        )
        msg.attach_alternative(html_content, "text/html")
        if attachment:
            msg.attach(
                attachment.filename,
                attachment.content,
                attachment.mimetype,
            )
        return msg
