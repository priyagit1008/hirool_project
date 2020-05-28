
# Create your models here.
# python imports
import uuid
# django/rest_framwork imports
from django.db import models
# project level imports
from libs.models import TimeStampedModel
from accounts.users.models import User
# third party imports
from model_utils import Choices
from jsonfield import JSONField


class LeaveType(TimeStampedModel):
	LEAVE_TYPE = Choices(
		('Planned', 'PLANNED'),
		('Emergancy', 'EMERGANCY'),
		('Sick', 'SICK'),
	)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	available_leaves = models.IntegerField()
	message = models.TextField(blank=True)

class  LeaveTracker(TimeStampedModel):
	id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
	user = models.ForeignKey(User,on_delete=models.PROTECT)




