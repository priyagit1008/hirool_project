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
    # queryset = Candidate.objects.all()

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


    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, ],)
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


        
    
    @action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
    def candidate_list(self,request):
        print(request.user.id)
        data = self.get_serializer(self.queryset,many=True).data
        return Response(data, status.HTTP_200_OK)


    @action(methods=['get'],detail=False,permission_classes=[IsAuthenticated,],)
    def candidate_get(self,request):
        try:
            id = request.GET["id"]
            serializer = self.get_serializer(self.service.get_candidate(id))
            return Response(serializer.data,status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


        # print(request.user.id)
        # id = request.GET.get("id")
        # try:
        #     # d = Candidate.objects.get(id=candidate_id)
        #     data = self.get_serializer(self.service.get_candidate(id))
        #     return Response(data, status.HTTP_200_OK)
        # except Exception as e:
        #     print(e)
        #     return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)


    # id = request.GET["id"]
    #         serializer = self.get_serializer(self.service.get_user(id))

    @action(methods=['get','put'],detail=False,permission_classes=[IsAuthenticated,],)
    def candidate_update(self,request):
        try:
           
            data=request.data
            id=data['id']
            # id_obj=Candidate.objects.get(id=id)
            serializer=self.get_serializer(self.service.update_candidate(id),data=request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                raise ParseException(BAD_REQUEST,serializer.errors)
            else:
                # serializer.update(id_obj,serializer.data)
                serializer.save()
                print(serializer.data)
                return Response(serializer.data,status.HTTP_200_OK)
        except Candidate.DoesNotExist:
            return Response({"status": "Invalid Id"}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # print(str(e))
            raise
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)

    @action(
        methods=['get'],
        detail= False,
        permission_classes=[],
        )
    def download_file(self,request, encoding='utf8'):
        try:   
            candidate_id=request.GET["id"]
            resume_name = Candidate.objects.get(id=candidate_id).Resume
            if not candidate_id.is_valid():
                raise ParseException("invalide id",BAD_REQUEST)
            else:
                resume_path = os.path.join(MEDIA_ROOT,str(resume_name))
                FilePointer = open(resume_path,'rb')
                response = HttpResponse((FilePointer),content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="%s.docx"' %(resume_name)
                return response
        except Exception as e:
            return Response({"status": "Not Found"}, status.HTTP_404_NOT_FOUND)





# this line request id to downlode a file.
# this line match the input id and in table stored id if both id 
            # match using that id this will get resume colume from table.
# this is prints the where this id is located that id path and folder
# resume_path is a veriable MEDIA_ROOT this imported from settings in 
            # settings MEDIA_ROOT caintains base_dir and resume name include id and 
  # FilePointer is veriable it open the  file from  that resume_path in 
            # read mode 







  # file_path = os.path.join(settings.MEDIA_ROOT, path)
  #   if os.path.exists(file_path):
  #       with open(file_path, 'rb') as fh:
  #           response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
  #           response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
  #           return response
  #   raise Http404
