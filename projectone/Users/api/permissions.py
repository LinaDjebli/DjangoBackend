from rest_framework.permissions import BasePermission


class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return  bool(request.user and request.user.is_client)


class IsAgencyUser(BasePermission):
    def has_permission(self, request, view):
        return  bool(request.user and request.user.is_agency)    
    
 
class IsGuideUser(BasePermission):
    def has_permission(self, request, view):
        return  bool(request.user and request.user.is_guide)   