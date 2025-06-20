from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.is_staff
        return False
    
    def has_object_permission(self, request, view, obj):
        pass

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user and request.user.is_authenticated and request.user.is_staff
    
class IsAdminOrReadOnlyForStaff(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user and request.user.is_authenticated:
            return request.user.staff
        
        return request.user.is_admin