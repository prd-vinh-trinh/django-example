from base.services import BaseService, Mailing, Verification
from django.conf import settings
from django.utils.translation import gettext as _


class AuthService(BaseService):

    @classmethod
    def verify_user_email(
        cls,
        email,
        first_name,
        last_name=None,
        role_ids=None,
    ):
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
        if role_ids:
            data.update({"role_ids": role_ids})
        token = Verification.create_token(data=data)
        api_host = settings.API_HOST
        admin_scheme = (
            "http"
            if api_host.startswith("localhost") or api_host[0].isdigit()
            else "https"
        )
        link = f"{admin_scheme}://{api_host}/auth/verify?token={token}"
        data = {
            "template": "auth/emails/email_verify_register.html",
            "subject": _("Create account"),
            "context": {
                "email": email,
                "full_name": f"{first_name} {last_name}",
                "token": token,
                "link": link,
                # "logo": logo,
                "lang": "en"  # Todo make it dynamic
            },
            "to": [email],
        }
        message = Mailing.create_html_message(data=data)
        Mailing.asyn_send_message(message=message)
        return token
