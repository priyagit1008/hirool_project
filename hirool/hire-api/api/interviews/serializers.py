from rest_framework import serializers

# app level imports
from .models import Interview ,InterviewRound,InterviewStatus
from libs.helpers import time_it

from clients.models import Client




#interview serializer
class InterviewCreateRequestSerializer(serializers.Serializer):
	date = serializers.DateTimeField(required=True)
	location = serializers.CharField(required=True)
	client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(),required=False)
  

	# password = serializers.CharField(required=True, min_length=5)
	class Meta:
		model = Interview
		fields = (
			'id','client', 'job', 'interview_round', 'candidate', 'member',
			'date', 'location', 'interview_status'
		)

	def create(self, validated_data):
		interview= Interview.objects.create(**validated_data)

		# user.set_password(validated_data['password'])
		interview.save()

		return interview

class InterviewListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Interview
		
		fields = (
			'id','client', 'job', 'interview_round', 'candidate', 'member',
			'date', 'location', 'interview_status'
		)
		# write_only_fields = ('password',)
		# read_only_fields = ('id',)



#########################################################################




# inetrview_round serializer
class InterviewRoundRequestSerializer(serializers.Serializer):
	interview_round=serializers.CharField(required=True)

	class Meta:
		models = InterviewRound
		fields = '__all__'


	def create(self, validated_data):
		interview_round= InterviewRound.objects.create(**validated_data)
		interview_round.save()
		return interview_round

class InterviewRoundListSerializer(serializers.ModelSerializer):
	class Meta:
		model= InterviewRound
		fields= '__all__'


############################################################################





#interview status serializer
class InterviewStatusRequestSerializer(serializers.Serializer):
	status=serializers.CharField(required=True)

	class Meta:
		models = InterviewStatus
		fields = '__all__'


	def create(self, validated_data):
		interview_status= InterviewStatus.objects.create(**validated_data)
		interview_status.save()
		return interview_status

class InterviewStatusListSerializer(serializers.ModelSerializer):
	class Meta:
		model= InterviewStatus
		fields= '__all__'