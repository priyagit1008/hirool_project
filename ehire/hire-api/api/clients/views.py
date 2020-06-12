# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly,HiroolReadWrite
import json 


# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
)
from libs.exceptions import ParseException

# app level imports
from .models import Client, Job ,Clientindustry,Clientcategory

from .services import ClientServices

from .services import JobServices
from .services import ClientiIndustryServices,ClientCategoryServices

from .serializers import (
	ClientCreateRequestSerializer,
	ClientListSerializer,
	ClientUpdateSerializer,
	ClientindustryRequestSerializer,
	clientindustryListSerializer,
	ClientcategoryRequestSerializer,
	ClientcategoryListSerializer,
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
	permissions=(HiroolReadOnly,HiroolReadWrite)
	services = ClientServices()
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




	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated,],)
	def org(self, request):
		"""
		Returns clients account creations
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create client with", serializer.validated_data)

		client = serializer.create(serializer.validated_data)
		if client:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def org_details(self, request):
		"""
		Returns client details
		"""
		client_id = request.GET.get("id")
		try:
			client_obj = Client.objects.get(id=client_id)
			client_data = self.get_serializer(client_obj).data
			return Response(client_data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ])
	def org_list(self, request,**dict):
		"""
		Returns clients list

		"""
		try:

			filter_data = request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset(filter_data),many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)





	@action(methods=['get'],detail=False,permission_classes=[],)
	def client_dashboard(self,request):
		"""
		Returns total clients
		"""
		client_count = Client.objects.count()
		return Response({"Total_clients":client_count}, status.HTTP_200_OK)


	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated, ],)
	def org_update(self,request):
		"""
		Returns client update
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_client_service(id),data=request.data)
			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()    
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	

	@action(methods=['get', 'patch'],detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,],
	)
	def org_get(self, request):
		"""
		Return client singal data and groups
		"""
		try:
			id=request.GET["id"]
			serializer=self.get_serializer(self.services.get_client_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['get', 'patch'],detail=False,
		permission_classes=[IsAuthenticated,],
		)
	def client_column_jsondata(self, request):
		myfile= open('/home/priya/workspace/hire-api/api/libs/json_files/client_columns.json','r')
		jsondata = myfile.read()
		obj = json.loads(jsondata)
		print(str(obj))
		return Response(obj)
			# return Response(data)

		# file_path=('/home/priya/workspace/hire-api/api/libs/json_files/client_columns.json')
		# FilePointer = open(file_path,'rb')
		# return Response("client":FilePointer,status.HTTP_200_OK)
		# response =Response((FilePointer),content_type='')
		# return Response()
		# response['Content-Disposition'] = 'attachment; filename="%s.json"'
		# return response 



		# with open('/home/priya/workspace/hire-api/api/libs/json_files/client_columns.json', encoding='utf-8-sig') as json_file:
		# 	text = json_file.read()
		# 	json_data = json.load(text)
		# 	print(json_data)
		# 	return response({"json_data":json_data},status.HTTP_200_OK)


class ClientIndustryViewSet(GenericViewSet):
	"""docstring for interview"""

	services = ClientiIndustryServices()
	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_clientindustry': ClientindustryRequestSerializer,
		'clientindustry_get': clientindustryListSerializer,
		'clientindustry_list': clientindustryListSerializer,
	}

	def get_serializer_class(self):
		"""
		:return:
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_clientindustry(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		industry = serializer.create(serializer.validated_data)
		if industry:
			return Response(serializer.data,status.HTTP_201_CREATED)
		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def clientindustry_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_clientindustry_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	# def clientindustry_list(self, request):

	#   data = self.get_serializer(self.services.get_queryset(),many=True).data
	#   return Response(data, status.HTTP_200_OK)

class ClientCategoryViewSet(GenericViewSet):
	"""docstring for interview"""

	services = ClientCategoryServices()
	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_clientcategory': ClientcategoryRequestSerializer,
		'clientcategory_get': ClientcategoryListSerializer,
		'clientcategory_list': ClientcategoryListSerializer,
	}

	def get_serializer_class(self):
		"""
		:return:
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_clientcategory(self, request):

		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		category = serializer.create(serializer.validated_data)
		if category:
			return Response(serializer.data,status.HTTP_201_CREATED)
		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
	def clientcategory_get(self, request):
		"""
		Return client profile data and groups
		"""
		try:
			id= request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_clientcategory_service(id))
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



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



	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def job(self, request):
		"""
		Returns jd details
		"""
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create job with", serializer.validated_data)

		job_obj = serializer.create(serializer.validated_data)
		if job_obj:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ],)
	def job_get(self, request):
		"""
		Returns single jd details
		"""
		try:
			id = request.GET["id"]
			serializer=self.get_serializer(self.services.get_job_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	# @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite],)
	# def job_list(self, request):
	#   """
	#   """
	#   data = self.get_serializer(self.queryset, many=True).data
	#   return Response(data, status.HTTP_200_OK)

	

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated,],)
	def job_list(self, request,**dict):
		"""
		Returns all jd details
		"""
		try:
			filter_data = request.query_params.dict()
			serializer=self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(methods=['get','put'], detail=False, permission_classes=[IsAuthenticated,HiroolReadWrite ],)
	def job_update(self,request):
		"""
		Returns jd edit
		"""
		try:
			data=request.data
			id=data["id"]
			serializer=self.get_serializer(self.services.update_job_service(id),data=request.data)
			if not serializer.is_valid():
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


	@action(methods=['get'],detail=False,permission_classes=[],)
	def job_dashboard(self,request):
		"""
		Returns total number of jds
		"""
		job_count = Job.objects.count()
		return Response({"Total_jobs":job_count}, status.HTTP_200_OK)