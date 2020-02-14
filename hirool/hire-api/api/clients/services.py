# app levelimports
from .models import Client,Job

class ClientServices:

	def get_queryset(self):
		return Client.objects.all()

	def get_client_service(self,id):
		try:
			return Client.objects.get(id = id)
		except Client.DoesNotExists:
			return Response("invalid id")


	def update_client_service(self,id):
		try:
			return Client.objects.get(id = id)
		except Client.DoesNotExists:
			return Response("invalid id")

class JobServices:
	"""docstring for JobService"""
	def get_queryset(self):
		return Job.objects.all()

	def get_job_service(self,id):
		try:
			return Job.objects.get(id=id)
		except Job.DoesNotExists:
			return Response("invalid id")
			
	def update_job_service(self,id):
		try:
			return Job.objects.get(id = id)
		except Job.DoesNotExists:
			return Response("invalid id")
