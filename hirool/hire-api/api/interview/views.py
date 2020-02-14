from django.shortcuts import render

# Create your views here.



# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
)

from libs.exceptions import ParseException

# app level imports
from .models import Interview,InterviewRound,InterviewStatus
# from .services import ClientServices

from .serializers import (
	InterviewCreateRequestSerializer,
	InterviewListSerializer,
	InterviewRoundRequestSerializer,
	InterviewRoundListSerializer,
	InterviewStatusRequestSerializer,
	InterviewStatusListSerializer
)

from .services import InterviewServices
from .services import InterviewRound_Services
from .services import InterviewStatus_Services

class InterviewViewSet(GenericViewSet):
	"""docstring for ClassName"""
	
	services = InterviewServices()

	queryset = services.get_queryset()



	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']


	serializers_dict = {
		'add': InterviewCreateRequestSerializer,
		'Interview_get': InterviewListSerializer,
		'interview_list': InterviewListSerializer,
		}



	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create interview with", serializer.validated_data)

		interview = serializer.create(serializer.validated_data)
		if interview:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'],detail=False,permission_classes=[IsAuthenticated, ],)
	def interview_get(self, request):
		# try:
		id=request.GET["id"]
		print(id)
		serializer=self.get_serializer(self.services.get_interview_service(id))
		return Response(serializer.data,status.HTTP_200_OK)
		# except Exception as e:
		#   return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def interview_list(self,request):
		print(request.user.id)
		data = self.get_serializer(self.queryset,many=True).data
		return Response(data, status.HTTP_200_OK)

###################################################################################



class InterviewRoundViewSet(GenericViewSet):
	"""docstring for interview"""

	services = InterviewRound_Services()

	queryset = services.get_queryset()


	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']


	serializers_dict = {
		'add_round': InterviewRoundRequestSerializer,
		'round_get': InterviewRoundListSerializer,
		'round_list':InterviewRoundListSerializer,
		}



	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add_round(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create round with", serializer.validated_data)

		interview = serializer.create(serializer.validated_data)
		if interview:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get', 'patch'],detail=False,permission_classes=[IsAuthenticated, ],)
	def round_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id=request.GET["id"]
			serializer=self.get_serializer(self.services.get_Round_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def round_list(self,request):
		print(request.user.id)
		data = self.get_serializer(self.queryset,many=True).data
		return Response(data, status.HTTP_200_OK)

	
class InterviewStatusViewSet(GenericViewSet):

	services = InterviewStatus_Services()

	queryset = services.get_queryset()


	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']


	serializers_dict = {
		'add_status': InterviewStatusRequestSerializer,
		'status_get': InterviewStatusListSerializer,
		'status_list':InterviewStatusListSerializer,
		}
	

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add_status(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create status with", serializer.validated_data)

		interview = serializer.create(serializer.validated_data)
		if interview:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'],detail=False,permission_classes=[IsAuthenticated, ],)
	def status_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id=request.GET["id"]
			serializer=self.get_serializer(self.services.get_status_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
	
	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def status_list(self,request):
		print(request.user.id)
		data = self.get_serializer(self.queryset,many=True).data
		return Response(data, status.HTTP_200_OK)
