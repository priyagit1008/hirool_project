from django.shortcuts import render
# import os
from docx import Document
import unicodedata
import os,io
from django.conf import settings

# from django.conf.settings import BASE_DIR
# import urllib2

# django imports
# from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
# from .serializers import MyFileSerializer


# from .forms import uplodefile_form

# app level imports
from .models import Candidate
# from accounts.users import permissions
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite




from .serializers import (
	CandidateCreateRequestSerializer,
	CandidateListSerializer,
	CandidateListSerializer,
	CandidateUpdateSerializer,
	# DownloadResumeSerializer
	# CandidateResumeSerializer,


	# CandidateFileSerializer
	)
from .services import CandidateServices

# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		
)
from api.default_settings import MEDIA_ROOT 

from libs.exceptions import ParseException
import codecs 

# Create your views here.

class CandidateViewSet(GenericViewSet):
	"""docstring for candidateViewset"""
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = CandidateServices()

	queryset = services.get_queryset()



	filter_backends = (filters.OrderingFilter,)
	# authentication_classes = (TokenAuthentication,)
	parser_class = (FileUploadParser,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict={
			'candidate':CandidateCreateRequestSerializer,
			'candidate_list':CandidateListSerializer,
			'candidate_get':CandidateListSerializer,
			'candidate_update':CandidateUpdateSerializer,
			# 'download_file':DownloadResumeSerializer,
			# 'upload_file':CandidateResumeSerializer
			# 'candidate_file_view':CandidateFileSerializer,
			}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def candidate(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if not serializer.is_valid():
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)
		print("create candidate with", serializer.validated_data)

		candidate= serializer.create(serializer.validated_data)
		if candidate:

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND) 


		
	
	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def candidate_list(self,request):
		data = self.get_serializer(self.queryset,many=True).data
		return Response(data, status.HTTP_200_OK)



	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,HiroolReadOnly],)
	# @permission_required('action.user','action.action','action.permission')
	def candidate_get(self,request):
		try:
			id = request.GET["id"]
			serializer = self.get_serializer(self.services.get_candidate_service(id))
			# print(serializer)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get','put'],detail=False,permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def candidate_update(self,request):
		try:
		   
			data=request.data
			id=data['id']
			serializer=self.get_serializer(self.services.update_candidate_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				# serializer.update(id_obj,serializer.data)
				serializer.save()
				print(serializer.data)
				return Response(serializer.data,status.HTTP_200_OK)
		# except Candidate.DoesNotExist:
		#   return Response({"status": "Invalid Id"}, status.HTTP_404_NOT_FOUND)
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get'],
		detail= False,
		permission_classes=[],
		)
	def download_file(self,request, encoding='utf8'):
		try:   
			id=request.GET["id"]
			resume_name = Candidate.objects.get(id=id).resume
			resume_path = os.path.join(MEDIA_ROOT,str(resume_name))
			FilePointer = open(resume_path,'rb')
			response = HttpResponse((FilePointer),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
			response['Content-Disposition'] = 'attachment; filename="%s.docx"' %(resume_name)
			return response
		except Exception as e:
			raise
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'],detail=False,
		permission_classes=[])
	def candidate_filter(self,request):
		try:
			# experience= request.GET.get("work_experience")
			skills=request.GET.get("tech_skills")
			# print(experience)
			# print(ctc)
			candidate_obj = Candidate.objects.filter(tech_skills=skills)
			print(candidate_obj)
			print("user request ssuccessfull")
			return Response({"status": "success"}, status.HTTP_200_OK)
		except Exception as e:
			print("user request not ssuccessfull")
			return Response({"status": " not success"}, status.HTTP_404_NOT_FOUND)













	# @action(methods=['get'],detail=False,permission_classes=[])
	# def filter_skills(self,request):
	# 	try:
	# 		skills=request.GET.get("tech_skills")
	# 		print(tech_skills)
	# 		skill_obj=Candidate.objects.filter(Q())


		pass
	
