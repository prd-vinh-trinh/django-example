import datetime
from urllib.parse import urlparse
from typing import Any, List, Tuple

from base.services import BaseService, Mailing, Verification
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q, Value
from django.db.models.functions import Collate
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class UserService(BaseService):
    @classmethod
    def validate_data(cls, data: dict) -> Tuple[List[Any], List[Any]]:
        valid_data = []
        valid_emails = []
        duplicated_emails = []
        for user in data:
            email = user.get("email")
            if email in valid_emails:
                duplicated_emails.append(email)
            else:
                valid_data.append(user)
                valid_emails.append(email)

        return valid_data, duplicated_emails

    @classmethod
    def verify_user_email(
        cls,
        email,
        first_name,
        last_name=None,
        role_ids=None,
    ):
        data= {
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
        link = f"{admin_scheme}://{api_host}/user/verify?token={token}"
        default_host = settings.DEFAULT_HOST
        default_scheme = (
            "http"
            if default_host.startswith("localhost") or default_host.startswith("127.0.0.1")
            else "https"
        )
        logo = f"{default_scheme}://{default_host}/static/favicon.ico"
        data = {
            "template": "users/emails/verify_user_email.html",
            "subject": _("Create Pandosima Docs account"),
            "context": {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "token": token,
                "link": link,
                "logo": logo,
                "lang": "en" #Todo make it dynamic
            },
            "to": [email],
        }
        message = Mailing.create_html_message(data=data)
        Mailing.asyn_send_message(message=message)
