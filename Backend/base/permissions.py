from rest_framework.permissions import BasePermission


class ScopedPermission(BasePermission):

    def get_required_scope(self, request, view):
        if hasattr(view, 'required_scopes'):
            func_name = request.method.lower()
            return view.required_scopes.get(func_name, None)
        return None

    def has_permission(self, request, view):
        token = request.auth
        if token:
            token_scopes = token.get('scope', '').split()
            required_scope = self.get_required_scope(request, view)

            if required_scope:
                return required_scope in token_scopes
        return False
