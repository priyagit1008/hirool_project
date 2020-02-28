from .models import User,UserPermissions,Permissions,Actions

class UserServices:

	def get_queryset(self):
		return User.objects.all()

	def get_user(self,id):
		try:
			return User.objects.get(id = id)
		except User.DoesNotExists:
			return Response("invalid id")


	def update_user(self,id):
		try:
			return User.objects.get(id = id)
		except User.DoesNotExists:
			return Response("invalid id")



###########################################################################


class userpermissions_service:
	"""docstring for ClassName"""
	def get_queryset(self):
		return UserPermissions.objects.all()

	def get_userpermission_service(self,id):
		try:
			return UserPermissions.objects.get(id = id)
		except UserPermissions.DoesNotExists:
			return Response("invalid id")



class permission_service:
	"""docstring for permission_service"""
	def get_queryset(self):
		return Permissions.objects.all()




class action_service:
	"""docstring for ClassName"""
	def get_queryset(self):
		return Actions.objects.all()




		
		