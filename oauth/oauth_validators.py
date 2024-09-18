import json
from datetime import datetime
from jwcrypto import jwk, jwt
from jwcrypto.common import JWException
from jwcrypto.jwt import JWTExpired
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauthlib.common import verify_signed_token
from .tokens import JWTAccessToken
from django.contrib.auth import get_user_model

from oauth2_provider.models import (
    get_access_token_model,
    get_id_token_model,
)
IDToken = get_id_token_model()
AccessToken = get_access_token_model()
User = get_user_model()

class CustomOAuth2Validator(OAuth2Validator):
    def validate_bearer_token(self, token, scopes, request):
        if self.validate_bearer_jwt_token(token, scopes, request):
            return True
        return super().validate_bearer_token(token, scopes, request)
    
    def validate_id_token(self, token, scopes, request):
        """
        When users try to access resources, check that provided id_token is valid
        """
        if not token:
            return False

        id_token = self._load_id_token(token)
        if not id_token:
            return False

        if not id_token.allow_scopes(scopes):
            return False
        
        request.scopes = scopes
        if(isinstance(id_token, JWTAccessToken)):
            request.client_id = id_token.client_id
            user_id = id_token.user_id
            request.user_id = user_id
            request.access_token = AccessToken(
                user_id=user_id,
                application_id = id_token.client_id,
                token=token,
                expires=id_token.expires,
                scope=id_token.scope,
            )
            # Todo: Improve this to avoid hitting database
            user = User.objects.get(pk=user_id) if user_id else None
            request.user = user
            return True

        request.client = id_token.application
        request.user = id_token.user
        # this is needed by django rest framework
        # request.access_token = id_token
        return True

    def _load_id_token(self, token):
        key = self._get_key_for_token(token)
        if not key:
            return None
        try:
            jwt_token = jwt.JWT(key=key, jwt=token)
            claims = json.loads(jwt_token.claims)
            jti = claims.get("jti")
            if jti is None:
                return JWTAccessToken(claims)
            return IDToken.objects.get(jti=jti)
        except (JWException, JWTExpired, IDToken.DoesNotExist) as e:
            print(e)
            return None

    # Set `oidc_claim_scope = None` to ignore scopes that limit which claims to return,
    # otherwise the OIDC standard scopes are used.

    def get_additional_claims(self, request):
        return {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "full_name": ' '.join([request.user.first_name, request.user.last_name]),
            "email": request.user.email,
        }
    
    # If we use jwt token for accesstoken
    def validate_bearer_jwt_token(self, token, scopes, request):
        key = self._get_key_for_token(token)
        if not key:
            return False
        
        try:
            jwt_token = jwt.JWT(key=key, jwt=token)
            claims = json.loads(jwt_token.claims)
            user_id = claims.get("sub", None)
            scope = claims.get("scope", None)
            client_id = claims.get("aud", None)
            unix_timestamp = float(claims.get("exp", None))
            expires = datetime.fromtimestamp(unix_timestamp)
            # scope = " ".join(payload.get("scope", None))
            request.user_id = user_id
            request.client_id = client_id
            request.scopes = claims.get("scope", None)
            request.access_token = AccessToken(
                user_id=user_id,
                token=token,
                scope=scope,
                application_id=client_id,
                expires=expires
            )
            return True
        except Exception:
            return False