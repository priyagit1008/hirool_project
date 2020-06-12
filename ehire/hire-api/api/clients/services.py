# app levelimports
import json
from django.db.models import Q

from django.core import serializers
from .models import Client,Job,Clientindustry,Clientcategory

class ClientServices:

	def get_queryset(self,filter_data):
		return Client.objects.filter(**filter_data)

	def get_client_service(self,id):
		return Client.objects.get(id=id)

	def update_client_service(self,id):
		return Client.objects.get(id = id)



class ClientiIndustryServices:

	def get_queryset(self,filter_data):
		return Clientindustry.objects.filter(**filter_data)

	def get_clientindustry_service(self,id):
		return Clientindustry.objects.get(id=id)

	def update_clientindustry_service(self,id):
		return Clientindustry.objects.get(id = id)



class ClientCategoryServices:

	def get_queryset(self,filter_data):
		return Clientcategory.objects.filter(**filter_data)

	def get_clientcategory_service(self,id):
		return Clientcategory.objects.get(id=id)

	def update_clientcatgory_service(self,id):
		return Clientcategory.objects.get(id = id)




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
