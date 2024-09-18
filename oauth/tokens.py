from datetime import datetime
from oauthlib import common
from django.utils import timezone


def signed_token_generator(private_pem, **kwargs):
    """
    :param private_pem:
    """
    def signed_token_generator(request):
        request.claims = kwargs
        if request.scope is None and request.refresh_token_instance is not None:
            scope = request.refresh_token_instance.access_token.scope if request.refresh_token_instance.access_token else None
            request.scope = scope
        request.claims.update(
            {
                "sub": str(request.user.id),
                "aud": request.client_id,
                "iat": timezone.now(),
            },
        )
        return common.generate_signed_token(private_pem, request)

    return signed_token_generator

class JWTAccessToken():
    def __init__(self, claims):
        self.scope = claims["scope"]
        self.client_id = claims["aud"]
        self.user_id = claims["sub"]
        unix_timestamp = int(claims.get("exp", None))
        self.expires = datetime.utcfromtimestamp(unix_timestamp)
    
    def allow_scopes(self, scopes):
        """
        Check if the token allows the provided scopes

        :param scopes: An iterable containing the scopes to check
        """
        if not scopes:
            return True

        provided_scopes = set(self.scope.split())
        resource_scopes = set(scopes)

        return resource_scopes.issubset(provided_scopes)
    
    @property
    def scopes(self):
        """
        Returns a dictionary of allowed scope names (as keys) with their descriptions (as values)
        """
        # Don't move this import to global scope, because it it lazay object.
        from oauth2_provider.scopes import get_scopes_backend
        all_scopes = get_scopes_backend().get_all_scopes()
        token_scopes = self.scope.split()
        return {name: desc for name, desc in all_scopes.items() if name in token_scopes}
