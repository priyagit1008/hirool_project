import unicodedata
import os,io
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.core.mail import EmailMessage,send_mail
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string


from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Candidate
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
from .serializers import (
	CandidateCreateRequestSerializer,
	CandidateListSerializer,
	CandidateListSerializer,
	CandidateUpdateSerializer,
	)
from .services import CandidateServices
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		
)
from libs import (
				# redis_client,
				otpgenerate,
				mail,
				)
from api.default_settings import MEDIA_ROOT 

from libs.exceptions import ParseException
import codecs 

# Create your views here.

class CandidateViewSet(GenericViewSet):
	"""docstring for candidateViewset"""
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = CandidateServices()
	filter_backends = (filters.OrderingFilter,)
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
			}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[],)
	def candidate(self,request):
		"""
		Returns candidate account creation
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)
		print("create candidate with", serializer.validated_data)
		candidate= serializer.create(serializer.validated_data)
		if candidate:
			msg_plain = render_to_string('email_message.txt',{"user":candidate.name})
			msg_html = render_to_string('email.html',{"user":candidate.name})
			# mail.send_mail(msg_plain,"hi",candidate.email)
			send_mail('Hirool',msg_plain,settings.EMAIL_HOST_USER,[candidate.email],html_message=msg_html,)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND) 


		
	
	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def candidate_list(self,request,**dict):
		"""
		Returns candidate list
		"""
		try:
			filter_data=request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)
		# data = self.get_serializer(self.queryset,many=True).data
		# return Response(data, status.HTTP_200_OK)




	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,HiroolReadOnly],)
	def candidate_get(self,request):
		"""
		Returns single candidate details
		"""
		try:
			id = request.GET["id"]
			serializer = self.get_serializer(self.services.get_candidate_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get','put'],detail=False,permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def candidate_update(self,request):
		"""
		update candidate details
		"""
		try:
			data=request.data
			id=data['id']
			serializer=self.get_serializer(self.services.update_candidate_service(id),data=request.data)
			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get'],
		detail= False,
		permission_classes=[],
		)
	def download_file(self,request, encoding='utf8'):
		"""
		Download candidate resume
		"""
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


	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def candidate_dashboard(self,request):
		"""
		Returns total candidate details
		"""
		candidate_count = Candidate.objects.count()
		return Response({"candidate":candidate_count}, status.HTTP_200_OK)

	@action(
		methods=['get'],
		detail=False,permission_classes=[],
	)
	def candidate_send_email(self,request,**dict):
		"""
		send mail api
		"""
		try:
			msg_plain = render_to_string('email_message.txt',{"user":candidate.email})
			msg_html = render_to_string('email.html',{"user":candidate.email})
			# print(request.user.name)
			mail.sendmail.delay(msg_plain,"hi",[request.user.email])
			send_mail(
				'Hirool',
				msg_plain,
				'priyapatil1421997@gmail.com',
				[candidate.email],
				html_message=msg_html,
				)
			return Response("hi")
		except Exception as e:
			raise
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)