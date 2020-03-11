# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from django.db.models import Q
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite



# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import ParseException
# from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model  # If used custom user model
# from django.contrib.auth import authenticate

# app level imports
from .models import Client, Job

from .services import ClientServices

from .services import JobServices

from .serializers import (
	ClientCreateRequestSerializer,
	ClientListSerializer,
	ClientUpdateSerializer,
	JobCreateRequestSerializer,
	JobListSerializer,
	JobUpdateSerilaizer
)


# class CreateUserView(CreateAPIView):
#     model = get_user_model()
#     permission_classes = [
#         permissions.AllowAny # Or anon users can't register
#     ]
#     serializer_class = UserRegSerializer


class ClientViewSet(GenericViewSet):
	"""
	"""
	# queryset = Client.objects.all()

	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = ClientServices()

	# queryset = services.get_queryset()



	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'org': ClientCreateRequestSerializer,
		'org_details': ClientCreateRequestSerializer,
		'org_list': ClientListSerializer,
		'org_update': ClientUpdateSerializer,
		'org_get':ClientListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def org(self, request):
		"""
		"""
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create client with", serializer.validated_data)

		client = serializer.create(serializer.validated_data)
		if client:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def org_details(self, request):
		"""
		"""
		client_id = request.GET.get("id")
		try:
			client_obj = Client.objects.get(id=client_id)
			client_data = self.get_serializer(client_obj).data
			print("client_data", client_data)
			return Response(client_data, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ])
	def org_list(self, request):
		"""
		"""
		try:
			name=request.GET.get("name")
			category=request.GET.get("category")
			hiring_location=request.GET.get("hiring_location")
			serializer=self.get_serializer(self.services.get_queryset
				(name,category,hiring_location),many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)

			



	
	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def org_update(self,request):

		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_client_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				# serializer.update(id_obj,serializer.validated_data)
				serializer.save()
				print(serializer.validated_data)
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			# print(str(e))
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	

	@action(methods=['get', 'patch'],detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,HiroolReadOnly],
	)
	def org_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id=request.GET["id"]
			serializer=self.get_serializer(self.services.get_client_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	# @action(methods=['get'],detail=False,
	#   permission_classes=[])
	# def filter_client(self,request):
	#   try:
	#       client_name= request.GET.get("name")
	#       client_category=request.GET.get("category")
	#       client_obj = Client.objects.all().filter(Q(name=client_name) | Q(category=client_category))
	#       print(client_name)
	#       print(client_category)
	#       print("user request ssuccessfull")
	#       return Response({"status": "success"}, status.HTTP_200_OK)
	#   except Exception as e:
	#       print("user request not ssuccessfull")
	#       return Response({"status": " not success"}, status.HTTP_404_NOT_FOUND)






	@action(methods=['get'],detail=False,
		permission_classes=[])
	def client_filter(self,request):
		try:
			client_name=request.GET.get("name")
			client_category=request.GET.get("category")
			client_obj=Client.objects.filter(name=client_name,category=client_category)
			print(client_obj)
			return Response({"status": "success"}, status.HTTP_200_OK)
		except Exception as e:
			print("user request not ssuccessfull")
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)





	# @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated, ],)
	# def org_details(self, request):
	#     """
	#     """
	#     serializer = self.get_serializer(data=request.data)

	#     if not serializer.is_valid():
	#         raise ParseException(BAD_REQUEST, serializer.errors)
	#     try:
	#         print(serializer.validated_data)
	#         d = Client.objects.get(id="input_id")
	#         data = self.get_serializer(d).data
	#         return Response(data, status.HTTP_200_OK)
	#     except Exception as e:
	#         print(e)
	#         return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


class JobViewSet(GenericViewSet):
	"""
	"""
	# queryset = Job.objects.all()
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'job': JobCreateRequestSerializer,
		'job_get': JobCreateRequestSerializer,
		'job_list': JobListSerializer,
		'job_update':JobUpdateSerilaizer,

	}

	# from .services import JobServices
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = JobServices()

	# queryset = services.get_queryset()

  
	 
	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)



	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def job(self, request):
		"""
		"""
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if not serializer.is_valid():
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create job with", serializer.validated_data)

		job_obj = serializer.create(serializer.validated_data)
		if job_obj:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadOnly ],)
	def job_get(self, request):
		"""
		"""
		try:
			id = request.GET["id"]
			serializer=self.get_serializer(self.services.get_job_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite],)
	# def job_list(self, request):
	# 	"""
	# 	"""
	# 	data = self.get_serializer(self.queryset, many=True).data
	# 	return Response(data, status.HTTP_200_OK)

	

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite],)
	def job_list(self, request):
		"""
		"""
		try:
			location=request.GET.get("location")
			job_title=request.GET.get("job_title")
			min_relevant_exp=request.GET.get("min_relevant_exp")
			min_ctc=request.GET.get("min_ctc")
			max_ctc=request.GET.get("max_ctc")
			serializer=self.get_serializer(self.services.get_queryset
				(location,job_title,min_relevant_exp,min_ctc,max_ctc), many=True)
			# print(serializer)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)

			
	




	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def job_update(self,request):
		"""
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_job_service(id),data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				# serializer.update(id_obj,serializer.validated_data)
				serializer.save()
				print(serializer.validated_data)
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)
	


	@action(methods=['get'],detail=False, 
		permission_classes =[])
	def job_filter(self,request):
		try:
			client_id=request.GET.get("client_id")
			location=request.GET.get("location")
			job_title=request.GET.get("job_title")
			job_obj=Job.objects.filter(location=location,job_title=job_title,client_id=client_id)
			print(job_obj.id)
			return Response({"status": "success"}, status.HTTP_200_OK)
		except Exception as e:
			print("user request not ssuccessfull")
			return Response({"status": " not success"}, status.HTTP_404_NOT_FOUND)

	# @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated, ],)
	# def job_details(self, request):
	#     """
	#     """
	#     serializer = self.get_serializer(data=request.data)

	#     if not serializer.is_valid():
	#         raise ParseException(BAD_REQUEST, serializer.errors)
	#     try:
	#         print(serializer.validated_data)
	#         d = Client.objects.get(id="input_id")
	#         data = self.get_serializer(d).data
	#         return Response(data, status.HTTP_200_OK)
	#     except Exception as e:
	#         print(e)
	#         return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)
