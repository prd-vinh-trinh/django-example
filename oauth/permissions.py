import logging

from oauth2_provider.contrib.rest_framework.permissions import TokenMatchesOASRequirements


log = logging.getLogger("oauth2_provider")


class TokenHasActionScope(TokenMatchesOASRequirements):
    """
    :attr:alternate_required_scopes: dict keyed by view action name with value: iterable alternate scope lists.
    For each method, a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
       'get': [['read']],
       'update': [['create1','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']],
    }

    TODO: DRY: subclass TokenHasScope and iterate over values of required_scope?
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):  # OAuth 2
            required_alternate_scopes = self.get_required_alternate_scopes(request, view)

            m = view.action.lower()
            if m in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {0}".format(
                        required_alternate_scopes[m]
                    )
                )
                for alt in required_alternate_scopes[m]:
                    if token.is_valid(alt):
                        return True
                return False
            else:
                log.warning("no scope alternates defined for method {0}".format(m))
                return False

        assert False, (
            "TokenHasActionScope requires the"
            "`oauth.rest_framework.OAuth2Authentication` authentication "
            "class to be used."
        )