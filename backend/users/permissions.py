from django.conf import settings
from rest_framework.permissions import BasePermission

class CanSignUpload(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm("images.sign_upload")