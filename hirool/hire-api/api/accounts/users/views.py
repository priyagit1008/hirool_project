# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import HiroolReadOnly
import math, random 
from django.core.mail import send_mail



# app level imports
from .models import User,Actions,Permissions,UserPermissions
from .serializers import (
	UserLoginRequestSerializer,
	# UserVerifyRequestSerializer,
	# UserSerializer,
	UserRegSerializer,
	UserListSerializer,
	UserUpdateRequestSerializer,
	UserPermissionCreateRequestSerializer,
	UserPermissionsListSerializer,
	PermissionCreateRequestSerializer,
	PermissionsListSerializer,
	ActionCreateRequestSerializer,
	ActionListSerializer
)

from .services import UserServices
from .services import userpermissions_service
from .services import permission_service
from .services import action_service


# project level imports
from libs.constants import (
		BAD_REQUEST,
		BAD_ACTION,
		# ParseException

)
# from accounts.constants import COULD_NOT_SEND_OTP, USER_NOT_REGISTERED
from libs.exceptions import ParseException
# from libs.helpers import time_it

# from rest_framework import permissions
# from rest_framework.generics import CreateAPIView
# from django.contrib.auth import get_user_model  # If used custom user model
from django.contrib.auth import authenticate


class UserViewSet(GenericViewSet):
	"""
	"""
	# queryset = User.objects.all()

	permissions=(HiroolReadOnly,)
	services = UserServices()

	# queryset = services.get_queryset()

	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'login': UserLoginRequestSerializer,
		'register': UserRegSerializer,
		'list_exec': UserListSerializer,
		'exec': UserListSerializer,
		'exec_update': UserUpdateRequestSerializer,
		# 'list': UserListSerializer,
	}



	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[])
	def register(self, request):
		"""
		"""
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("registering user with", serializer.validated_data)

		user = serializer.create(serializer.validated_data)
		if user:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({}, status.HTTP_200_OK)

	@action(methods=['post'], detail=False,permission_classes=[])
	def login(self, request):
		"""
		"""
		# old app hack
		try:
			int(request.META['HTTP_X_APP_VERSION'])
		except Exception as e:
			print(e)
			raise ParseException({"detail": "Please update to new version."})

		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print(serializer.validated_data)
		user = authenticate(
			email=serializer.validated_data["email"],
			password=serializer.validated_data["password"])

		if not user:
			return Response({'error': 'Invalid Credentials'},
							status=status.HTTP_404_NOT_FOUND)
		token = user.access_token
		return Response({'token': token},
						status=status.HTTP_200_OK)





	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
	def logout(self, request):

		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def list_exec(self, request,**dict):
		"""
		Return user profile data and groups
		"""
		try:
			filter_data=request.query_params.dict()
			print(filter_data)
			serializer=self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			raise
			return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)


		# data = self.get_serializer(self.get_queryset(), many=True).data
		# return Response(data, status.HTTP_200_OK)



	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated,],
	)
	def exec(self, request):
		"""
		Return user profile data and groups
		"""
		
		try:
			id = request.GET["id"]
			print(id)
			serializer = self.get_serializer(self.services.get_user(id))
			print(serializer.data)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(
		methods=['get','put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def exec_update(self, request):
		"""
		Return user profile data and groups
		"""
		try:
		   
			data=request.data
			id=data['id']
			serializer=self.get_serializer(self.services.update_user(id),data=request.data)
			# serializer=self.get_serializer(data=request.data)
			if not serializer.is_valid():
				print(serializer.errors)
				raise ParseException(BAD_REQUEST,serializer.errors)
			else:
				serializer.save()
				print(serializer.data)
				return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			print(str(e))
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	# @action(
	# 	methods=['put'],
	# 	detail=False,
	# 	# url_path='image-upload',
	# 	permission_classes=[IsAuthenticated, ],
	# )
	# def email_address(self):
	# 	email_address = self.cleaned_data.get('email_address')
	# 	if Test.objects.filter(email_address__iexact=email_address).count() == 0:
	# 		raise forms.ValidationError("Your email address not exist")
	# 		return email_address


	@action(
		methods=['put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def change_pass(self,request):
			data=request.data
			password=data['password']
			user = User.objects.get(id=request.user.id)
			user.set_password(password)
			user.save()
			return Response({"status": "success"}, status.HTTP_200_OK)
	# def filter_role(self,request):
	#   data=request.data
	#   role=data['role']
	#   user=User
	#   pass



###################################################################################
class UserPermissionsViewSet(GenericViewSet):
	"""
	"""

	services = userpermissions_service()

	queryset = services.get_queryset()
  
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_userpermissions': UserPermissionCreateRequestSerializer,
		'list_userpermission':UserPermissionsListSerializer,
		'get_userpermission':UserPermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add_userpermissions(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create userpermissions with", serializer.validated_data)

		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)






	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated, ],)
	def list_userpermission(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)


	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
	def get_userpermission(self,request):
		try:
			id = request.GET["id"]
			serializer = self.get_serializer(self.services.get_userpermission_service(id))
			return Response(serializer.data,status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


###############################################################################

class PermissionsViewSet(GenericViewSet):
	"""
	"""

	services = permission_service()

	queryset = services.get_queryset()
  
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_permissions': PermissionCreateRequestSerializer,
		'list_permission':PermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add_permissions(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create permissions with", serializer.validated_data)

		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated, ],)
	def list_permission(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)

############################################################################

class ActionViewSet(GenericViewSet):
	"""
	"""

	services = action_service()

	queryset = services.get_queryset()
  
	filter_backends = (filters.OrderingFilter,)
	authentication_classes = (TokenAuthentication,)

	ordering_fields = ('id',)
	ordering = ('id',)
	lookup_field = 'id'
	http_method_names = ['get', 'post', 'put']

	serializers_dict = {
		'add_actions': ActionCreateRequestSerializer,
		'list_actions':ActionListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
	def add_actions(self,request):
		serializer = self.get_serializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid() is False:
			print(serializer.errors)
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create actions with", serializer.validated_data)

		action= serializer.create(serializer.validated_data)
		if action:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'],detail=False,permission_classes=[IsAuthenticated, ],)
	def list_actions(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)




























   #      except Exception as e:
   #          raise
   #      else:
   #          pass
   #      finally:
   #          pass
   #      data=request.data
   #      data["id"]=request.User.id
   #      d=User.objects.get(id=request.User.id)
   #      serializer = self.get_serializer(data=request.data)
   #      if not serializer.is_valid():
   #              raise ParseException(BAD_REQUEST, serializer.errors)
   #              try:
   #                  serializer.save()
   #                  return Response(serializer.data, status.HTTP_200_OK)
   #                  print(serializer.data)
   #              except Exception as e:
   #                  return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




   # try:
   #          data=request.data
   #          client_id=data['client_id']
   #          client_obj=myclients.objects.get(client_id=client_id)
   #          serializer = addclientSerializer(client_obj,data=data)
   #          if serializer.is_valid():
   #              serializer.save()
   #              return Response(serializer.data)
   #          else:
   #              return Response(serializer.errors)
   #      except:
   #          return Response({"status":"Bad request"})
