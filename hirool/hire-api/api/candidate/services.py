# app levelimports
from .models import Candidate

class CandidateServices:



	def get_queryset(self):
		return Candidate.objects.all()


	def get_candidate_service(self,id):
		try:
			return Candidate.objects.get(id = id)
		except Candidate.DoesNotExists:
			return Response("invalid id")


	def update_candidate_service(self,id):
		try:
			return Candidate.objects.get(id = id)
		except Candidate.DoesNotExists:
			return Response("invalid id")

