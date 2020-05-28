# Create your views here.
# django imports
from django.conf import settings

from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.users.permissions import HiroolReadOnly, HiroolReadWrite
from django.template.loader import render_to_string
from django.core.mail import send_mail

# project level imports
from libs.constants import (
    BAD_REQUEST,
    BAD_ACTION,
)
from libs.exceptions import ParseException

# app level imports
from .models import Interview, InterviewRound, InterviewStatus
# project level imports
from clients.models import Client, Job
from accounts.models import User
from candidate.models import Candidate
# from .services import ClientServices

from .serializers import (
    InterviewCreateRequestSerializer,
    InterviewGetSerializer,
    InterviewListSerializer,
    InterviewUpdateSerilaizer,
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
    permissions = (HiroolReadOnly, HiroolReadWrite)
    services = InterviewServices()

    # queryset = services.get_queryset()

    filter_backends = (filters.OrderingFilter,)
    authentication_classes = (TokenAuthentication,)

    ordering_fields = ('id',)
    ordering = ('id',)
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put']

    serializers_dict = {
        'interview_add': InterviewCreateRequestSerializer,
        'interview_get': InterviewGetSerializer,
        'interview_list': InterviewGetSerializer,
        'interview_update': InterviewUpdateSerilaizer,
    }

    def get_serializer_class(self):
        """
		"""
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, HiroolReadWrite], )

    def interview_add(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:

            raise ParseException(BAD_REQUEST, serializer.errors)
        interview = serializer.create(serializer.validated_data)

        if interview:
            msg_plain = render_to_string('email_message.txt', {"user": interview.candidate.name})
            msg_html = render_to_string('email.html', {"user": interview.candidate.name})
            send_mail('Hirool', msg_plain, settings.EMAIL_HOST_USER, [interview.candidate.email],html_message=msg_html, )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)



    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated,], )
    def interview_get(self, request):
        try:
            id= request.GET.get('id', None)
            if not id:
                return Response({"status": "Failed", "message":"id is required"})
            else:
                serializer = self.get_serializer(self.services.get_interview_service(id))
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, HiroolReadWrite], )
    def interview_list(self, request, **dict):
        try:
            filter_data = request.query_params.dict()
            serializer = self.get_serializer(self.services.interview_filter_service(filter_data), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


    @action(methods=['put'], detail=False, permission_classes=[IsAuthenticated, HiroolReadWrite], )
    def interview_update(self, request):
        """
        Return user profile data and groups
        """
        try:

            data = request.data
            id= request.GET.get('id', None)
            if not id:
                return Response({"status": "Failed", "message":"id is required"})
            serializer = self.get_serializer(self.services.update_interview_service(id), data=request.data)
            if not serializer.is_valid():
                raise ParseException(BAD_REQUEST, serializer.errors)
            else:
                serializer.save()
                print(serializer.data)
                return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)



    @action(methods=['get'], detail=False, permission_classes=[])
    def interview_filter(self, request):
        try:
            id = request.GET["id"]
            print(id)
            serializer = self.get_serializer(self.services.interview_filter_service(id))
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            raise
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


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
        'round_list': InterviewRoundListSerializer,
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
    def add_round(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)

            interview = serializer.create(serializer.validated_data)
        if interview:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
    def round_get(self, request):
        """
		Return client profile data and groups
		"""
        try:
            id= request.GET.get('id', None)
            if not id:
                return Response({"status": "Failed", "message":"id is required"})
            else:
                serializer = self.get_serializer(self.services.get_Round_service(id))
                return Response(serializer.data, status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
    def round_list(self, request):
        data = self.get_serializer(self.queryset, many=True).data
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
        'status_list': InterviewStatusListSerializer,
    }

    def get_serializer_class(self):
        """
		"""
        try:
            return self.serializers_dict[self.action]
        except KeyError as key:
            raise ParseException(BAD_ACTION, errors=key)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ], )
    def add_status(self, request):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() is False:
            raise ParseException(BAD_REQUEST, serializer.errors)
            interview = serializer.create(serializer.validated_data)
            if interview:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"status": "error"}, status.HTTP_404_NOT_FOUND)


    @action(methods=['get', 'patch'], detail=False, permission_classes=[IsAuthenticated, ], )
    def status_get(self, request):
        """
		Return client profile data and groups
		"""
        try:
            id= request.GET.get('id', None)
            if not id:
                return Response({"status": "Failed", "message":"id is required"})
            else:
                serializer = self.get_serializer(self.services.get_status_service(id))
                return Response(serializer.data, status.HTTP_200_OK)
            except Exception as e:
                return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ], )
    def status_list(self, request):

        data = self.get_serializer(self.queryset, many=True).data
        return Response(data, status.HTTP_200_OK)
