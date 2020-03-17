# app levelimports
import json
from django.db.models import Q

from django.core import serializers
from .models import Client,Job

class ClientServices:

	def get_queryset(self,filter_data):

		
		print(dict)
		return Client.objects.filter(**filter_data)


		# return Client.objects.filter(Q(name__isnull=True) | Q(name=name)
		# if(name="",)
		# if(name==None):
		#   name=""
		# if(category==None):
		#   category=""
		# else:
		#   return Client.objects.all()

		# if name is not None:
		# 	queryset = Client.objects.filter(name=name)
		# 	return queryset
		# if(name==None):
		# 	queryset = Client.objects.all()
		# 	return queryset





	def get_client_service(self,id):
		return Client.objects.get(id=id)

	def update_client_service(self,id):
		return Client.objects.get(id = id)

class JobServices:
	"""docstring for JobService"""
	# def get_queryset(self):
	#   return Job.objects.all()

	def get_queryset(self,filter_data):

		return Job.objects.filter(**filter_data)

	def get_job_service(self,id):
		return Job.objects.get(id=id)
			
	def update_job_service(self,id):
		return Job.objects.get(id = id)
