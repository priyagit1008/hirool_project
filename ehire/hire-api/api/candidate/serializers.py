# django imports
from rest_framework import serializers

# app level imports
from .models import Candidate
from libs.helpers import time_it

class CandidateCreateRequestSerializer(serializers.Serializer):
	"""docstring for ClassName"""
	name = serializers.CharField(required=True)
	email = serializers.EmailField(required=False)
	
	profile_link = serializers.CharField(required=False)
	mobile = serializers.IntegerField(required=True)
	sslc= serializers.CharField(required=True)
	puc = serializers.CharField(required=True)
	degree = serializers.CharField(required=True)
	master = serializers.CharField(required=True)
	sslc_per = serializers.CharField(required=True)
	puc_per=serializers.CharField(required=True)
	degree_per=serializers.CharField(required=True)
	master_per = serializers.CharField(required=True)
	# certification = serializers.CharField(required=False)
	work_experience = serializers.CharField(required=True)
	previous_company = serializers.CharField(required=True)
	work_location=serializers.CharField(required=True)
	address = serializers.CharField(required=True)
	resume = serializers.FileField(required=True)
	previous_ctc = serializers.FloatField(required=False)
	expected_ctc = serializers.FloatField(required=False)
	notice_days=serializers.IntegerField(default=60)

	# is_already_on_notice = serializers.IntegerField(required=False)
	tech_skills = serializers.JSONField(required=False)
	status = serializers.CharField(required=True)

	class Meta:
		model = Candidate
		fields = ['name','email','profile_link','mobile','address',
		'sslc','puc','degree','master','sslc_per','puc_per','degree_per',
		'master_per','work_experience','previous_company','work_location',
		'address','resume','previous_ctc','expected_ctc','notice_days','tech_skills'
		'status']          

	def create(self, validated_data):
		candidate= Candidate.objects.create(**validated_data)

		# user.set_password(validated_data['password'])
		candidate.save()

		return candidate
class CandidateListSerializer(serializers.ModelSerializer):
	"""
	"""
	class Meta:
		model=Candidate
		fields = ['name','email','profile_link','mobile','address',
		'sslc','puc','degree','master','sslc_per','puc_per','degree_per',
		'master_per','work_experience','previous_company','work_location',
		'address','resume','previous_ctc','expected_ctc','notice_days','tech_skills'
		'status']

class CandidateUpdateSerializer(serializers.ModelSerializer):
	name = serializers.CharField(required=True)
	email = serializers.EmailField(required=False)
	resume = serializers.FileField(required=True)
	candidate_url = serializers.CharField(required=True)
	mobile = serializers.IntegerField(required=True)
	address = serializers.CharField(required=True)
	min_ctc = serializers.FloatField(required=False)
	max_ctc = serializers.FloatField(required=False)
	notice_days=serializers.IntegerField(default=60)

	# is_already_on_notice = serializers.IntegerField(required=False)
	tech_skills = serializers.JSONField(required=False)
	location=serializers.CharField(required=True)

	def update(self,instance,validated_data):
		instance.name =  validated_data.get('name', instance.name)
		instance.email =  validated_data.get('email', instance.email)
		instance.resume =  validated_data.get('Resume', instance.Resume)
		instance.candidate_url =  validated_data.get('candidate_url', instance.candidate_url)
		instance.mobile =  validated_data.get('mobile', instance.mobile)
		instance.address =  validated_data.get('address', instance.address)
		instance.min_ctc =  validated_data.get('min_ctc', instance.min_ctc)
		instance.max_ctc =  validated_data.get('max_ctc', instance.max_ctc)
		instance.notice_days =  validated_data.get('notice_days', instance.notice_days)
		instance.save()
		return instance

	class Meta:
		"""docstring for Meta"""
		model=Candidate
		fields = ['name','email','profile_link','mobile','address',
		'sslc','puc','degree','master','sslc_per','puc_per','degree_per',
		'master_per','work_experience','previous_company','work_location',
		'address','resume','previous_ctc','expected_ctc','notice_days','tech_skills'
		'status' ]
			

class DownloadResumeSerializer(serializers.ModelSerializer):
	"""docstring for DownloadResumeSerializer"""
	class Meta:
		model=Candidate
		fields=['Resume']


		
		
