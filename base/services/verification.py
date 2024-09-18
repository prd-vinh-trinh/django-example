from datetime import datetime

import jwt
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _

from .base import BaseService


class Verification(BaseService):
    @staticmethod
    def get_header():
        return {"alg": "HS256", "typ": "JWT"}

    @staticmethod
    def get_secret_key():
        return settings.SECRET_KEY

    @staticmethod
    def create_token(data, life_time=3600):
        if not isinstance(data, dict):
            raise ValidationError(detail=_("Invalid format"))
        
        payload = data
        payload.update()
        {
            "iat": datetime.now().timestamp(),
            "exp": datetime.now().timestamp() + life_time
        }

        token = jwt.encode(payload, Verification.get_secret_key(), algorithm="HS256")
        return token

    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, Verification.get_secret_key(), algorithms=["HS256"])
        if 'iat' in payload:
            del payload['iat']
        
        if 'exp' in payload:
            exp = int(payload.get("exp"))
            if datetime.now().timestamp() < exp:
                raise Exception(_('Token expired!'))
            del payload['exp']
        return payload