from rest_framework import serializers

# app level imports
from .models import Interview ,InterviewRound,InterviewStatus
from libs.helpers import time_it




#interview serializer
class InterviewCreateRequestSerializer(serializers.Serializer):
	date = serializers.DateTimeField(required=True)
	location = serializers.CharField(required=True)
  

	# password = serializers.CharField(required=True, min_length=5)
	class Meta:
		model = Interview
		fields = (
			'id','client_id', 'job_id', 'interview_round_id', 'candidate_id', 'member_id',
			'date', 'location', 'interview_status_id'
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
			'id','client_id', 'job_id', 'interview_round_id', 'candidate_id', 'member_id',
			'date', 'location', 'interview_status_id'
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