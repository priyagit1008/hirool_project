# app levelimports
from rest_framework import serializers
import json

from .models import Candidate

class CandidateServices:



	def get_queryset(self,tech_skills,work_experience):
		# return Candidate.objects.all()
		# return Candidate.objects.filter(tech_skills=tech_skills).values()
		return Candidate.objects.filter(tech_skills=tech_skills,work_experience=work_experience).values()
	
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

