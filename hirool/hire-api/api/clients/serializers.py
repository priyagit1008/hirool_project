# django imports
from rest_framework import serializers

# app level imports
from .models import Client, Job,Clientindustry,Clientcategory
from libs.helpers import time_it


class ClientCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    name = serializers.CharField(required=True)
    web_link = serializers.CharField(required=True)
    ceo= serializers.CharField(required=False)
    founder= serializers.CharField(required=False)
    founded_on= serializers.CharField(required=False)
    email= serializers.CharField(required=True)
    mobile= serializers.CharField(required=True)
    revenue= serializers.CharField(required=False)
    latest_funding= serializers.CharField(required=False)
    headquarter = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    profile_desc= serializers.CharField(required=False)
    aggrement_doc= serializers.CharField(required=False)
    status= serializers.CharField(required=False)
    industry= serializers.CharField(required=False)
    category= serializers.CharField(required=False)
    

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Client
        fields = (
            'id','name', 'web_link', 'headquarter', 'address', 'industry','category',
            'business_type', 'status', 'profile_desc', 'aggrement_doc',
            'extra'
        )

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)

        # user.set_password(validated_data['password'])
        client.save()

        return client


class ClientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # Tuple of serialized model fields (see link [2])
        fields = '__all__'
        # fields = (
        #     'id', 'name', 'web_link', 'headquarter', 'address', 'category',
        #     'business_type', 'status', 'profile_desc'
        # )
        # write_only_fields = ('password',)
        # read_only_fields = ('id',)

class ClientDrowpdownGetSerializer(serializers.Serializer):
    value = serializers.CharField(source='address',required=True, min_length=2)
    label = serializers.CharField(source='address',required=True, min_length=2)
    class Meta:
        model = Client
        fields = ('id','value','label')
        


class ClientUpdateSerializer(serializers.ModelSerializer):
    """docstring for ClientUpdateSerializer"""
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    web_link = serializers.CharField(required=True)
    ceo= serializers.CharField(required=False)
    founder= serializers.CharField(required=False)
    founded_on= serializers.CharField(required=False)
    email= serializers.CharField(required=True)
    mobile= serializers.CharField(required=True)
    revenue= serializers.CharField(required=False)
    latest_funding= serializers.CharField(required=False)
    headquarter = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    profile_desc= serializers.CharField(required=False)
    aggrement_doc= serializers.CharField(required=False)
    status= serializers.CharField(required=False)
    industry= serializers.CharField(required=False)
    category= serializers.CharField(required=False)
    

    def update(self, instance, validated_data):
        # instance.id =  validated_data.get('id', instance.id)
        # instance.name =  validated_data.get('name', instance.name)
        # instance.web_link = validated_data.get('web_link', instance.web_link)
        # instance.ceo = validated_data.get('ceo', instance.ceo)
        # instance.founder = validated_data.get('founder', instance.founder)
        # instance.founded_on = validated_data.get('founded_on', instance.founded_on)
        # instance.email = validated_data.get('email', instance.email)
        # instance.mobile = validated_data.get('mobile', instance.mobile)
        # instance.revenue = validated_data.get('revenue', instance.revenue)
        # instance.latest_funding = validated_data.get('latest_funding', instance.latest_funding)
        # instance.headquarter = validated_data.get('headquarter', instance.headquarter)
        # instance.address = validated_data.get('address', instance.address)
        # instance.profile_desc = validated_data.get('profile_desc', instance.profile_desc)
        # instance.aggrement_doc = validated_data.get('aggrement_doc', instance.aggrement_doc)
        # instance.status = validated_data.get('status', instance.status)
        # instance.industry = validated_data.get('industry', instance.industry)
        # instance.category = validated_data.get('category', instance.category)
        for attr ,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

    class Meta:
        model = Client
        fields = '__all__'
        # fields = ('id','name','web_link','address')

    # def update(self):
    #     data = self.validated_data
    #     print(data)

    #     fields=('id','name','web_link','address')
class ClientindustryRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    client_industry=serializers.CharField(required=True)

    class Meta:
        models = Clientindustry
        fields = ('id','client_industry')

    def create(self, validated_data):
        industry= Clientindustry.objects.create(**validated_data)
        return industry

class clientindustryListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientindustry
        fields= '__all__'





class ClientcategoryRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    client_category=serializers.CharField(required=True)

    class Meta:
        models = Clientcategory
        fields = '__all__'

    def create(self, validated_data):
        category= Clientcategory.objects.create(**validated_data)
        return category

class ClientcategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientcategory
        fields= '__all__'


class clientindustryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientindustry
        fields = ('client_industry')

class clientcategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Clientcategory
        fields=('client_category')

class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model =Client
        fields='__all__'
                


class JobCreateRequestSerializer(serializers.Serializer):
    """
    ClientCreateRequestSerializer
    """
    client_id = serializers.CharField(required=True)
    job_title = serializers.CharField(required=True)
    jd_url = serializers.CharField(required=False)
    tech_skills = serializers.JSONField(required=False)
    job_location = serializers.CharField(required=False)
    job_type = serializers.CharField(required=False)
    min_exp = serializers.IntegerField(required=False)
    max_exp = serializers.IntegerField(required=False)
    min_notice_period = serializers.IntegerField(required=False)
    max_notice_period = serializers.IntegerField(required=False)
    # status = serializers.CharField(required=False)
    min_ctc = serializers.FloatField(required=False)
    max_ctc = serializers.FloatField(required=False)

    qualification = serializers.CharField(required=False)
    percentage_criteria=serializers.IntegerField(required=False)
    status=serializers.CharField(required=False)
    jd_extra = serializers.JSONField(required=False)

    # password = serializers.CharField(required=True, min_length=5)
    class Meta:
        model = Job
        fields = (
            'client_id', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
        )

    def create(self, validated_data):
        job_obj = Job.objects.create(**validated_data)
        # client_obj = Client.objects.get(validated_data['client'])
        # job_obj.client = client_obj
        print(job_obj)
        job_obj.save()
        return job_obj

class clientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields= ('name','email','mobile','ceo','address') 

class JobGetSerializer(serializers.ModelSerializer):
    client=clientGetSerializer()
    class Meta:
        model =Job
        fields=('id','client', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
            )


class JobListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        # Tuple of serialized model fields (see link [2])
        # fields = ( "id", "username", "password", )
        fields = (
          'id','client_id', 'job_title', 'jd_url', 'tech_skills', 'job_location', 'job_type',
            'min_exp', 'max_exp', 'min_notice_period', 'max_notice_period', 'min_ctc', 'max_ctc',
            'qualification','percentage_criteria','status','jd_extra'
       
        )
        # write_only_fields = ('password',)
        # fields='__all__'
        read_only_fields = ('id',)

class JobUpdateSerilaizer(serializers.ModelSerializer):
    """docstring for JobUpdateSerilaizer"""
    id = serializers.CharField(required=True)

    client_id = serializers.CharField(required=False)
    job_title = serializers.CharField(required=True)
    jd_url = serializers.CharField(required=False)
    tech_skills = serializers.JSONField(required=False)
    job_location = serializers.CharField(required=False)
    job_type = serializers.CharField(required=False)
    min_exp = serializers.IntegerField(required=False)
    max_exp = serializers.IntegerField(required=False)
    min_notice_period = serializers.IntegerField(required=False)
    max_notice_period = serializers.IntegerField(required=False)
    # status = serializers.CharField(required=False)
    min_ctc = serializers.FloatField(required=False)
    max_ctc = serializers.FloatField(required=False)

    qualification = serializers.CharField(required=False)
    percentage_criteria=serializers.IntegerField(required=False)
    status=serializers.CharField(required=False)
    jd_extra = serializers.JSONField(required=False)
    # expiring_on = serializers.DateTimeField(required=False)

    def update(self, instance, validated_data):
        # instance.job_title =  validated_data.get('job_title', instance.job_title)
        # instance.jd_url =  validated_data.get('jd_url', instance.jd_url)
        # instance.tech_skills =  validated_data.get('tech_skills', instance.tech_skills)
        # instance.min_exp =  validated_data.get('min_exp', instance.min_exp)
        # instance.max_exp =  validated_data.get('max_exp', instance.max_exp)
        for attr ,value in validated_data.items():
            setattr(instance,attr,value)
            instance.save()
            return instance
        # instance.save()
        # return instance

        # instance.expiring_on =  validated_data.get('expiring_on', instance.expiring_on)

    class Meta:
        model = Job
        # fields = ('job_title','jd_url','tech_skills','min_exp','max_exp')
        # fields = (
        #     'id', 'client_id', 'job_title', 'jd_url', 'tech_skills', 'location', 'job_type',
        #     'min_exp', 'max_exp', 'min_relevant_exp', 'max_notice', 'min_ctc', 'max_ctc',
        #     'expiring_days', 'jd_extra'
        # )
        fields = '__all__'
        
        
        
        




