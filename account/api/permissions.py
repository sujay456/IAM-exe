from rest_framework import permissions


# class IsTokenValid(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         user_id = request.user.id            
#         is_allowed_user = True
#         token = request.auth.decode("utf-8")
#         try:
#             is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
#             if is_blackListed:
#                 is_allowed_user = False
#         except BlackListedToken.DoesNotExist:
#             is_allowed_user = True
#         return is_allowed_user