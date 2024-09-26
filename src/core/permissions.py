from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class CheckScopePermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the view has 'required_alternate_scopes'
        if hasattr(view, 'required_alternate_scopes'):
            required_scopes = view.required_alternate_scopes.get(view.action, [])
            
            user_scopes = self.get_user_scopes(request)

            for scope_group in required_scopes:
                if all(scope in user_scopes for scope in scope_group):
                    return True

            raise PermissionDenied("You do not have the required permissions.")
        return True

    def get_user_scopes(self, request):
        return request.user.get_scopes()
