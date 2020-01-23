from django.db import models

# Create your models here.

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField
# project level imports
from libs.models import TimeStampedModel
# import datetime
import uuid

# third party imports
from model_utils import Choices

class Interview(TimeStampedModel):
	"""docstring for Interview"""
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id =models.ForeignKey(Client,on_delete=models.PROTECT,related_name='client')
    job_id = models.ForeignKey(Job,on_delete=models.PROTECT,related_name='Job')
    interview_round_id = models.ForeignKey(Round,on_delete=models.PROTECT,related_name='Round')
    candidate_id = models.ForeignKey(Candidate,on_delete=models.PROTECT,
    	related_name='Candidate')
    member_id = models.ForeignKey(User,on_delete=models.PROTECT,related_name='User')
    date = models.DateTimeField()
    location = models.CharField()
    interview_status_id=model.ForeignKey(InterviewStatus,on_delete=models.PROTECT,related_name='InterviewStatus')
    # status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)


class Round(TimeStampedModel):
	"""docstring for Role"""
	INTERVIEW_ROUND= Choices(
		('FR','Online round'),
		('SR','Technical round'),
		('TR','HR round'),
		)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview_round=models.CharField(max_length=200,choices=INTERVIEW_ROUND)


class InterviewStatus(TimeStampedModel):
	"""docstring for Status"""
	STATUS = Choices(
		('FS','Processing'),
		('SS','Completed'),
		('TS','Sheduled'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)

		
						