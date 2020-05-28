# django imports
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import HiroolReadOnly
import math, random
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.conf import settings

# app level imports
from .models import User, Actions, Permissions, UserPermissions
# from templates 

from .serializers import (
	UserLoginRequestSerializer,
	UserRegSerializer,
	UserListSerializer,
	UserUpdateRequestSerializer,
	UserPassUpdateSerializer,

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
from libs import (
	# redis_client,
	otpgenerate,
	mail,
)
from libs.clients import (
	redis_client
)
from libs.exceptions import ParseException
from django.contrib.auth import authenticate


class UserViewSet(GenericViewSet):
	"""
	"""
	permissions = (HiroolReadOnly,)
	services = UserServices()
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
		'forgotpass': UserPassUpdateSerializer,
		'update_pass': UserPassUpdateSerializer,
	}

	def get_serializer_class(self):
		"""
		Returns serilizer class
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)


	@action(methods=['post'], detail=False, permission_classes=[])
	def register(self, request):
		"""
		Returns user account creations
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
			user = serializer.create(serializer.validated_data)
			if user:
				msg_plain = render_to_string('email_message.txt', {"user": user.first_name})
				msg_html = render_to_string('email.html', {"user": user.first_name})
				send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [user.email], html_message=msg_html)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


	@action(methods=['post'], detail=False, permission_classes=[])
	def login(self, request):
		"""
		Return user login
		"""
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

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
		"""
		Return user logout
		"""
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)

	@action(
		methods=['get'],
		detail=False,
		# url_path='image-upload',
		# permission_classes=[IsAuthenticated, ],
	)
	def list_exec(self, request, **dict):
		"""
		Return user list data and groups
		"""
		try:
			filter_data = request.query_params.dict()
			serializer = self.get_serializer(self.services.get_queryset(filter_data), many=True)
			return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	# data = self.get_serializer(self.get_queryset(), many=True).data
	# return Response(data, status.HTTP_200_OK)

	@action(
		methods=['get', 'patch'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def exec(self, request):
		"""
		Return user data and groups
		"""

		try:
			id = request.GET.get('id', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.get_user(id))
				return Response(serializer.data, status.HTTP_200_OK)
			except Exception as e:
				return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)




	@action(methods=['get', 'patch'],
			detail=False,
			# url_path='image-upload',
			permission_classes=[IsAuthenticated, ], )
	def profile(self, request):
		"""
		Return user profile data and groups
		"""
		response = {
			'first_name': request.user.first_name,
			'last_name': request.user.last_name,
			'email': request.user.email,
			'mobile': request.user.mobile,
			'image_url': request.user.image_url,
		}
		return Response(response, status.HTTP_200_OK)

	@action(
		methods=['get', 'put'],
		detail=False,
		url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def exec_update(self, request):
		"""
		Return user update data
		"""
		try:

			data = request.data
			id  = request.GET.get('email', None)
			if not id:
				return Response({"status": "Failed", "message":"id is required"})
			else:
				serializer = self.get_serializer(self.services.update_user(id), data=request.data)
				if not serializer.is_valid():
				raise ParseException(BAD_REQUEST, serializer.errors)
			else:
				serializer.save()
				return Response(serializer.data, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['put'],
		detail=False,
		# url_path='image-upload',
		permission_classes=[IsAuthenticated, ],
	)
	def change_pass(self, request):
		"""
		Returns user change password
		"""
		data = request.data
		password = data['password']
		user = User.objects.get(id=request.user.id)
		user.set_password(password)
		user.save()
		return Response({"status": "success"}, status.HTTP_200_OK)

	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def send_otp(self, request):
		"""
		send otp api
		"""
		try:
			email = request.GET.get('email', None)
			if not email:
				return Response({"status": "Failed", "message":"email  is required"})
			else:  
				user_obj= User.objects.get(email=email)
				otp = otpgenerate.otpgen(self)
				msg_plain = render_to_string('email_message.txt', {"user":otp})
				msg_html = render_to_string('password_reset_email.html', {"user": request.user.email})
				redis_client.store_data(email, otp)
				send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [request.user.email], html_message=msg_html, )
				return Response({"status": "email sent"}, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ], )
	def send_email(self, request):
		"""
		send mail api
		"""
		try:
			email = request.GET["email"]
			d = User.objects.get(email=email)
			subject, from_email, to = 'hello', settings.EMAIL_HOST_USER, [request.user.email]
			text_content = 'This is your otp.'
			first_name = request.user.first_name
			last_name = request.user.last_name
			role_id = request.user.role_id
			html_content = "your first name:" + first_name + " <br> last name:" + last_name + " <br> role_id:" + role_id + " <br>"
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			return Response("hi")
		except Exception as e:
			raise
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['put'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def forgotpass(self, request):
		"""
		Returns forgot password
		"""
		try:
			data = request.data
			self.object = User.objects.get(email=data["email"], is_active=True)

			if not redis_client.key_exists(data["email"]):
				print(redis_client.key_exists(data["email"]))
				return Response({"status": "Bad Otp"}, status=status.HTTP_400_BAD_REQUEST)

			if not redis_client.get_Key_data(data["email"]).decode("utf-8") == data["reset_otp"]:
				return Response({"status": "Bad Otp"}, status=status.HTTP_400_BAD_REQUEST)

			redis_client.delete_Key_data(data["email"])

			serializer = self.get_serializer(self.object, data=data)
			if not serializer.is_valid():
				return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)
			try:
				serializer.save()
				return Response({"status": "Successfully Updated password"}, status.HTTP_200_OK)
			except Exception as e:
				return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['put'],
		detail=False,
		permission_classes=[IsAuthenticated, ],
	)
	def update_pass(self, request):
		"""
		update new password with validatig old password
		"""
		data = request.data
		user_obj = User.objects.get(id=request.user.id)
		serializer = self.get_serializer(user_obj, data=data)
		if not serializer.is_valid():
			raise ParseException(BAD_REQUEST, serializer.errors)
		try:
			if not user_obj.check_password(data.get("old_password")):
				return Response({"old_password is Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
			serializer.save()
			return Response({"status": "Successfully Updated new password"}, status.HTTP_200_OK)
		except Exception as e:
			return Response({"status": str(e)}, status.HTTP_404_NOT_FOUND)

	@action(
		methods=['put'],
		detail=False,
		permission_classes=[IsAuthenticated, ],
	)
	def send_sms(self, request):
		frm = '+917483206167'
		to = '+919108258657'
		text = 'Please remember to pick up the bread before coming'
		send_text(text, frm, to)

	@action(
		methods=['get'],
		detail=False, permission_classes=[IsAuthenticated, ],
	)
	def user_dashboard(self, request):
		"""
		Return total users data
		"""
		user_count = User.objects.count()
		return Response({"users": user_count}, status.HTTP_200_OK)


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
		'list_userpermission': UserPermissionsListSerializer,
		'get_userpermission': UserPermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_userpermissions(self, request):
		"""
		Returns add userpermissions 
		"""
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)
		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def list_userpermission(self, request):
		"""
		Return all permission data
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def get_userpermission(self, request):
		"""
		Returns userpermission data
		"""
		try:
			id = request.GET["id"]
			serializer = self.get_serializer(self.services.get_userpermission_service(id))
			return Response(serializer.data, status.HTTP_200_OK)
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
		'list_permission': PermissionsListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_permissions(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		print("create permissions with", serializer.validated_data)

		permissions = serializer.create(serializer.validated_data)
		if permissions:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)

	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
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
		'list_actions': ActionListSerializer,

	}

	def get_serializer_class(self):
		"""
		"""
		try:
			return self.serializers_dict[self.action]
		except KeyError as key:
			raise ParseException(BAD_ACTION, errors=key)

	@action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
	def add_actions(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid() is False:
			raise ParseException(BAD_REQUEST, serializer.errors)

		action = serializer.create(serializer.validated_data)
		if action:
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
	def list_permission(self, request):
		"""
		Return user profile data and groups
		"""
		data = self.get_serializer(self.get_queryset(), many=True).data
		return Response(data, status.HTTP_200_OK)
	

# 	@action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
# 	def list_actions(self, request):
# 		"""
# 		Return user profile data and groups
# 		"""
# 		 data=request.data
# # user=User.objects.get(id=request.user.id).password
# print(user)
# if(old_password==user):
#   print("hi")
#   user.set_password(password)
#   user.save()
#   return Response({"status":"Successfully Updated password"}, status.HTTP_200_OK)
# else:
#   return Response({"status":"Not Found"},status.HTTP_404_NOT_FOUND)

# def filter_role(self,request):

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
