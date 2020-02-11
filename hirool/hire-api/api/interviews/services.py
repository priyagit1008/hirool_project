from .models import Interview,InterviewRound,InterviewStatus

class InterviewServices:

	def get_queryset(self):
		return Interview.objects.all()

	def get_interview(self,id):
		try:
			return Interview.objects.get(id = id)
		except Interview.DoesNotExists:
			return Response("invalid id")




class InterviewRound_Services:

	def get_queryset(self):
		return InterviewRound.objects.all()

	def get_Round(self,id):
		try:
			return InterviewRound.objects.get(id=id)
		except InterviewRound.DoesNotExists:
			return Response("invalid id")




class InterviewStatus_Services:
	def get_queryset(self):
		return InterviewStatus.objects.all()

	def get_status(self,id):
		try:
			return InterviewStatus.objects.get(id=id)
		except InterviewStatus.DoesNotExists:
			return Response("invalid id")
			
		
		

	