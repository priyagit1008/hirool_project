# django imports
from rest_framework import serializers

# app level imports
from .models import Candidate
from libs.helpers import time_it

class CandidateCreateRequestSerializer(serializers.Serializer):
	"""docstring for ClassName"""
	first_name = serializers.CharField(required=True)
	last_name=serializers.CharField(required=False)
	email = serializers.EmailField(required=True)
	candidate_url = serializers.CharField(required=False)
	mobile = serializers.IntegerField(required=True)
	dob=serializers.DateField(input_formats=['%d-%m-%Y',],required=False)
	gender=serializers.CharField(required=False)
	sslc_marks=serializers.CharField(required=False)
	puc_marks=serializers.CharField(required=False)
	bachelor_degree=serializers.CharField(required=False)
	bachelor_degree_course=serializers.CharField(required=False)
	bachelor_degree_marks=serializers.CharField(required=False)
	master_degree=serializers.CharField(required=False)
	master_degree_course=serializers.CharField(required=False)
	master_degree_marks=serializers.CharField(required=False)
	address = serializers.CharField(required=False)
	tech_skills= serializers.CharField(required=False)
	prefered_location=serializers.JSONField(required=False)
	previous_company=serializers.CharField(required=False)
	work_experience=serializers.CharField(required=False)
	current_ctc=serializers.FloatField(default=0.0,required=False)
	expected_ctc=serializers.FloatField(default=0.0,required=False)
	notice_period=serializers.CharField(required=False)
	resume=serializers.FileField(required=False)
	
	status = serializers.CharField(required=False)

	class Meta:
		model = Candidate
		fields = ('first_name','last_name','email ','candidate_url',
		'mobile','dob','gender','sslc_marks','puc_marks','puc_per','bachelor_degree',
		'bachelor_degree_course','bachelor_degree_marks','master_degree','master_degree_course','master_degree_marks',
		'address','tech_skills','prefered_location','previous_company','work_experience','current_ctc'
		'expected_ctc','notice_period','resume','status')        

	def create(self, validated_data):
		candidate= Candidate.objects.create(**validated_data)

		# user.set_password(validated_data['password'])

		return candidate


class CandidateListSerializer(serializers.ModelSerializer):
	"""
	"""
	class Meta:
		model=Candidate
		# fields = ('id','name','email','profile_link',
		# 'sslc','puc','degree','master','sslc_per','puc_per','degree_per',
		# 'master_per','certification','work_experience','previous_company','prepared_location',
		# 'address','resume','previous_ctc','expected_ctc','notice_days','tech_skills',
		# 'status')         

		fields= '__all__'  

# class CandidateDropdownListSerializer(serializers.ModelSerializer):
#   """
#   """
#   class Meta:
#       model=Candidate
#       fields = ('id','name')




class CandidateUpdateSerializer(serializers.ModelSerializer):
	id = serializers.CharField(required=True)
	first_name = serializers.CharField(required=True)
	last_name=serializers.CharField(required=False)
	email = serializers.EmailField(required=True)
	candidate_url = serializers.CharField(required=False)
	mobile = serializers.IntegerField(required=True)
	dob=serializers.DateField(input_formats=['%d-%m-%Y',],required=False)
	gender=serializers.CharField(required=False)
	sslc_marks=serializers.CharField(required=False)
	puc_marks=serializers.CharField(required=False)
	bachelor_degree=serializers.CharField(required=False)
	bachelor_degree_course=serializers.CharField(required=False)
	bachelor_degree_marks=serializers.CharField(required=False)
	master_degree=serializers.CharField(required=False)
	master_degree_course=serializers.CharField(required=False)
	master_degree_marks=serializers.CharField(required=False)
	address = serializers.CharField(required=False)
	tech_skills= serializers.CharField(required=False)
	prefered_location=serializers.JSONField(required=False)
	previous_company=serializers.CharField(required=False)
	work_experience=serializers.CharField(required=False)
	current_ctc=serializers.FloatField(default=0.0,required=False)
	expected_ctc=serializers.FloatField(default=0.0,required=False)
	notice_period=serializers.CharField(required=False)
	resume=serializers.FileField(required=False)
	
	status = serializers.CharField(required=False)

	def update(self,instance,validated_data):
		# instance.name =  validated_data.get('name', instance.name)
		# instance.email =  validated_data.get('email', instance.email)
		# # instance.resume =  validated_data.get('Resume', instance.Resume)
		# instance.profile_link =  validated_data.get('profile_link', instance.profile_link)
		# instance.mobile =  validated_data.get('mobile', instance.mobile)
		# instance.address =  validated_data.get('address', instance.address)
		# instance.previous_ctc =  validated_data.get('previous_ctc', instance.previous_ctc)
		# instance.expected_ctc =  validated_data.get('expected_ctc', instance.expected_ctc)
		# instance.notice_days =  validated_data.get('notice_days', instance.notice_days)
		# instance.tech_skills=validated_data.get('tech_skills',instance.tech_skills)
		# instance.prepared_location=validated_data.get('prepared_location',instance.prepared_location)
		for attr ,value in validated_data.items():
			setattr(instance,attr,value)
			instance.save()
			return instance

	class Meta:
		"""docstring for Meta"""
		model=Candidate
		fields='__all__'
		# fields = ['name','email','mobile','address','profile_link',
		# 'sslc','puc','degree','master','sslc_per','puc_per','degree_per',
		# 'master_per','work_experience','previous_company','prepared_location',
		# 'address','previous_ctc','expected_ctc','notice_days','tech_skills',
		# 'status' ]
			

class DownloadResumeSerializer(serializers.ModelSerializer):
	"""docstring for DownloadResumeSerializer"""
	class Meta:
		model=Candidate
		fields=['Resume']


		
		