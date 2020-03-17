from .models import Interview,InterviewRound,InterviewStatus
import json
from django.core import serializers
from clients.models import Client,Job
from accounts.models import User
from candidate.models import Candidate

class InterviewServices:

	# def get_queryset(self):
		# return Interview.objects.all()

	def get_interview_service(self,id):
		# interview_get=Interview.objects.get(id=id)
		return Interview.objects.get(id = id)

	def update_interview_service(self,id):
		return Interview.objects.get(id = id)


	def interview_filter_service(self,filter_data):
		return Interview.objects.filter(**filter_data).values()
		


		
class InterviewRound_Services:

	def get_queryset(self):
		return InterviewRound.objects.all()

	def get_Round_service(self,id):
		return InterviewRound.objects.get(id=id)




class InterviewStatus_Services:
	def get_queryset(self):
		return InterviewStatus.objects.all()

	def get_status_service(self,id):
		return InterviewStatus.objects.get(id=id)
		



# class Client_get_Service:
# 	def get_service(self,id):
# 		clients_get=Client.objects.get(id=id)


			