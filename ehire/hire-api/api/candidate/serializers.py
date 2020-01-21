# django imports
from rest_framework import serializers

# app level imports
from .models import Candidate
from libs.helpers import time_it

class CandidateCreateRequestSerializer(serializers.Serializer):
	"""docstring for ClassName"""
	name = serializers.CharField(required=True)
	email = serializers.EmailField(required=False)
	Resume = serializers.FileField(required=True)
	candidate_url = serializers.CharField(required=True)
	mobile = serializers.IntegerField(required=True)
	address = serializers.CharField(required=True)
	min_ctc = serializers.FloatField(required=False)
	max_ctc = serializers.FloatField(required=False)
	notice_days=serializers.IntegerField(default=60)

	# is_already_on_notice = serializers.IntegerField(required=False)
	tech_skills = serializers.JSONField(required=False)
	location=serializers.CharField(required=True)

	class Meta:
		model = Candidate
		fields = ['name','email','candidate_url','mobile','address',
		'min_ctc','max_ctc','notice_days','notice_days','is_already_on_notice',
		'tech_skills','location','status','Resume']          

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
		fields=('id','name','email','candidate_url','mobile','address',
			'min_ctc','max_ctc','notice_days','tech_skills','location','status',"Resume")


class CandidateUpdateSerializer(serializers.ModelSerializer):
	name = serializers.CharField(required=True)
	email = serializers.EmailField(required=False)
	Resume = serializers.FileField(required=True)
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
		instance.Resume =  validated_data.get('Resume', instance.Resume)
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
		fields = ['name','email','candidate_url','mobile','address',
		'min_ctc','max_ctc','notice_days','notice_days',
		'tech_skills','location','status','Resume'] 
			

class CandidateResumeSerializer(serializers.ModelSerializer):

	def update(self,instance,validated_data):
		instance.Resume =  validated_data.get('Resume', instance.Resume)
		instance.save()
		return  instance

	class Meta:
		"""docstring for Meta"""
		model=Candidate
		fields = ('id',"Resume") 



class DownloadResumeSerializer(serializers.ModelSerializer):
	"""docstring for DownloadResumeSerializer"""
	class Meta:
		model=Candidate
		fields=['Resume']


		
		