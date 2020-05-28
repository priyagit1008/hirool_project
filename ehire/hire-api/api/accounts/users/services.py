from .models import User,UserPermissions,Permissions,Actions

class UserServices:

	def get_queryset(self,filter_data):
		return User.objects.filter(**filter_data)
			
	def get_user(self,id):
		return User.objects.get(id = id)
		

	def update_user(self,id):
		return User.objects.get(id = id)
	

	def update_pass(self,id):
		return User.objects.get(id=id)
		

###########################################################################


class userpermissions_service:
	"""docstring for ClassName"""
	def get_queryset(self):
		return UserPermissions.objects.all()

	def get_userpermission_service(self,id):
		return UserPermissions.objects.get(id = id)

class permission_service:
	"""docstring for permission_service"""
	def get_queryset(self):
		return Permissions.objects.all()




class action_service:
	"""docstring for ClassName"""
	def get_queryset(self):
		return Actions.objects.all()	