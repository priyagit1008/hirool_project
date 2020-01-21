# django imports
from django.db import models
from django.contrib.postgres.fields import JSONField
# import datetime
import uuid

# project level imports
from libs.models import TimeStampedModel

# third party imports
from model_utils import Choices


from datetime import timedelta
from django.utils import timezone


def one_month_from_today():
    return timezone.now() + timedelta(days=30)


class Client(TimeStampedModel):
    """
    """

    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
    )

    CATEGORY = Choices(
        ('private', 'PRIVATE'),
        ('public', 'PUBLIC'),
    )

    BUSINESS_TYPE = Choices(
        ('product', 'PRODUCT'),
        ('service', 'SERVICE'),
        ('hybrid', 'HYBRID'),
    )
    # startup, IPO, Private, service, Product,
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=512, default=None, null=False, blank=False)
    web_link = models.CharField(max_length=512, default=None, null=True, blank=True)
    headquarter = models.CharField(max_length=512, default=None, null=False, blank=False)
    address = models.CharField(max_length=1024, default=None, null=False, blank=False)
    category = models.CharField(max_length=256, choices=CATEGORY, default=CATEGORY.private)
    business_type = models.CharField(
        max_length=256,
        choices=BUSINESS_TYPE,
        default=BUSINESS_TYPE.product
    )
    status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)

    # TODO this should be a file.
    profile_desc = models.CharField(max_length=1024, default=None, null=True, blank=True)
    # TODO this should be a file.
    aggrement_doc = models.CharField(max_length=1024, default=None, null=False, blank=False)

    # Should have emp_count, funding rounds, locations, fuctional area and all
    extra = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "{id}".format(id=self.id)

    def modify(self, payload):
        """
        This method will update tasks attributes
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()

    class Meta:
        app_label = 'clients'
        db_table = 'api_client'


class Job(TimeStampedModel):
    """
    The JD table
    """

    STATUS = Choices(
        ('active', 'ACTIVE'),
        ('inactive', 'INACTIVE'),
        ('on_hold', 'ON_HOLD'),
        ('expiried', 'EXPIRED'),
    )

    JOB_TYPE = Choices(
        ('permanent', 'PERMANENT'),
        ('contract', 'CONTRACT'),
        ('part_time', 'PART_TIME'),
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='client'
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_title = models.CharField(max_length=512, default=None, null=False, blank=False)
    jd_url = models.CharField(max_length=1024, default=None, blank=True)
    tech_skills = JSONField(default={}, blank=True, null=True)
    location = models.CharField(max_length=512, default=None, null=True, blank=True)
    job_type = models.CharField(max_length=256, choices=JOB_TYPE, default=JOB_TYPE.permanent)
    min_exp = models.IntegerField(default=0)  # number of years
    max_exp = models.IntegerField(default=60)  # number of years
    min_relevant_exp = models.IntegerField(default=0)  # number of years
    max_notice = models.IntegerField(default=60)  # number of days
    # role = models.CharField(max_length=512, default=None, null=True, blank=True)
    min_ctc = models.FloatField(default=0.0)  # LPA
    max_ctc = models.FloatField(default=1000.0)  # LPA

    expiring_days = models.IntegerField(default=180)
    status = models.CharField(max_length=256, choices=STATUS, default=STATUS.active)
    # May have Salary breakup, facilities, any other data
    jd_extra = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "{id}".format(id=self.id)

    def modify(self, payload):
        """
        This method will update tasks attributes
        """
        for key, value in payload.items():
            setattr(self, key, value)
        self.save()

    class Meta:
        app_label = 'clients'
        db_table = 'api_job'
