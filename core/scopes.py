from oauth.scopes import (
    scopes as oauth_scopes,
    default_scopes as oauth_default_scopes,
)

from api_users.scopes import (
    scopes as api_users_scopes,
    default_scopes as api_users_default_scopes,
)


scopes = {
    **oauth_scopes,
    **api_users_scopes,
}

default_scopes = {
    **oauth_default_scopes,
    **api_users_default_scopes,
}
