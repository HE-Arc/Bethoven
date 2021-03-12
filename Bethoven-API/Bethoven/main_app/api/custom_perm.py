from rest_framework import permissions

class isSelfUser(permissions.BasePermission):
    """
    Permission that verifies the user object is the user in the request (ex : for updating the user or accesing its data)
    """
    def has_permission(self, request, view):
        bethovenUser = view.get_object()
        return request.user.id == bethovenUser.user.id

class isBetOwner(permissions.BasePermission):
    """
    Permission that verifies the user object is the user in the request (ex : for updating the user or accesing its data)
    """
    def has_permission(self, request, view):
        bet = view.get_object()
        bethovenUser = bet.owner
        return request.user.id == bethovenUser.user.id