from .models import User

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