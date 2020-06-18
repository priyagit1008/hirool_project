# class Clientindustry(TimeStampedModel):
#     """docstring for Role"""
#     CLIENT_INDUSTRY= Choices(
#         ('FN','Finance'),
#         ('RS','Resources'),
#         ('PD','Products'),
#         ('HP','Health and public'),
#         )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     client_industry=models.CharField(max_length=200,choices=CLIENT_INDUSTRY)


# class Clientcategory(TimeStampedModel):
#     """docstring for Role"""
#     CLIENT_INDUSTRY = Choices(
#         ('PB','Public'),
#         ('PR','Private'),
#         ('OT','Other'),
#         )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     client_industry=models.CharField(max_length=200,choices=CLIENT_INDUSTRYs)



# class ClientStatus(TimeStampedModel):
#     """docstring for Status"""
#     STATUS = Choices(
#         ('FS','Processing'),
#         ('SS','Completed'),
#         ('TS','Sheduled'),
#     )
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     status = models.CharField(max_length=256, choices=STATUS, default=STATUS.FS)   



# class Client(TimeStampedModel):
#     """
#     """

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=512, default=None, null=False, blank=False)
#     web_link = models.CharField(max_length=512, default=None, null=True, blank=True)
#     ceo=models.CharField(max_length=512, default=None, null=False, blank=False)
#     founder=models.CharField(max_length=512, default=None, null=False, blank=False)
#     founded_on=models.CharField(max_length=512, default=None, null=False, blank=False)
#     email=models.CharField(max_length=512, default=None, null=False, blank=False)
#     mobile=models.CharField(max_length=512, default=None, null=False, blank=False)
#     revenue=models.CharField(max_length=512, default=None, null=False, blank=False)
#     latest_funding=models.CharField(max_length=512, default=None, null=False, blank=False)
#     headquarter = models.CharField(max_length=512, default=None, null=False, blank=False)
#     address = models.CharField(max_length=1024, default=None, null=False, blank=False)
#     profile_desc = models.CharField(max_length=1024, default=None, null=True, blank=True)
#     aggrement_doc = models.CharField(max_length=1024, default=None, null=False, blank=False)