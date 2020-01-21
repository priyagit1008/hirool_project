# app levelimports
from .models import Client,Job

class ClientServices:

	def get_queryset(self):
		return Client.objects.all()

	def get_client(self,id):
		try:
			return Client.objects.get(id = id)
		except Client.DoesNotExists:
			return Response("invalid id")


	def update_client(self,id):
		try:
			return Client.objects.get(id = id)
		except Client.DoesNotExists:
			return Response("invalid id")

class JobServices:
	"""docstring for JobService"""
	def get_queryset(self):
		return Job.objects.all()

	def get_job(self,id):
		try:
			return Job.objects.get(id=id)
		except Job.DoesNotExists:
			return Response("invalid id")

	def update_job(self,id):
		try:
			return Job.objects.get(id=id)
		except Exception as e:
			return Response("invalid id")
			raise