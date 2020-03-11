# app levelimports
import json
from django.core import serializers
from .models import Client,Job

class ClientServices:

	def get_queryset(self,name,category):
		return Client.objects.filter(name=name,category=category,
			hiring_location=hiring_location).values()


	def get_client_service(self,name):
		try:
			return Client.objects.get(id=id)
		except Client.DoesNotExists:
			return Response("invalid id")


	def update_client_service(self,id):
		try:
			return Client.objects.get(id = id)
		except Client.DoesNotExists:
			return Response("invalid id")

class JobServices:
	"""docstring for JobService"""
	# def get_queryset(self):
	# 	return Job.objects.all()

	def get_queryset(self,location,job_title,min_relevant_exp,min_ctc,max_ctc):
		return Job.objects.filter(location=location,job_title=job_title,min_relevant_exp=min_relevant_exp
			,min_ctc=min_ctc,max_ctc=max_ctc).values()


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
