from .models import Interview,InterviewRound,InterviewStatus
from clients.models import Client,Job
from accounts.models import User
from candidate.models import Candidate

class InterviewServices:

	def get_queryset(self):
		return Interview.objects.all()

	def get_interview_service(self,id):
		# interview_get=Interview.objects.get(id=id)
		try:
			return Interview.objects.get(id = id)
		except Interview.DoesNotExists:
			return Response("invalid id")

	def update_interview_service(self,id):
		try:
			return Interview.objects.get(id = id)
		except Interview.DoesNotExists:
			return Response("invalid id")



class InterviewRound_Services:

	def get_queryset(self):
		return InterviewRound.objects.all()

	def get_Round_service(self,id):
		try:
			return InterviewRound.objects.get(id=id)
		except InterviewRound.DoesNotExists:
			return Response("invalid id")




class InterviewStatus_Services:
	def get_queryset(self):
		return InterviewStatus.objects.all()

	def get_status_service(self,id):
		try:
			return InterviewStatus.objects.get(id=id)
		except InterviewStatus.DoesNotExists:
			return Response("invalid id")



class Client_get_Service:
	def get_service(self,id):
		clients_get=Client.objects.get(id=id)


			