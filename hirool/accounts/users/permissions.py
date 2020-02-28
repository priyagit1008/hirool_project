from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):

	def custom_permission(self, request, view, obj):
		print("hi")
		if request.method in permissions.SAFE_METHODS:

			# if User.objects.get(role=role_id).exists():
			if UserPermission.objects.filter(user=user,action=action,permission=permission).exists():

				return True
			else:
				return False
				
		else:
		#   UserPermission.objects.filter(user=user,action=action,permission=permission).exists():
			return False
			
			# return obj.user.id == request.user.id


