# django imports
from rest_framework import serializers
# from django.contrib.auth import get_user_model  # If used custom user model

# app level imports
from .models import User
from libs.helpers import time_it


class UserLoginRequestSerializer(serializers.ModelSerializer):
    """
    UserLoginSerializer
    """
    # mobile = serializers.IntegerField(
    #     min_value=5000000000,
    #     max_value=9999999999
    # )
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)

    class Meta:
        model = User
        fields = ('email','password','access_token')
        # fields = (
        #     'first_name', 'last_name', 'mobile', 'access_token',
        #     'is_active', 'email', 'image_url'
        # )


# class UserSerializer(serializers.ModelSerializer):
#     """
#     UserSerializer
#     """
#     access_token = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = (
#             'first_name', 'last_name', 'mobile', 'access_token',
#             'is_active', 'email', 'image_url'
#         )

#     def get_access_token(self, user):
#         """
#         returns users access_token
#         """
#         return user.access_token


class UserRegSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=5)
    first_name = serializers.CharField(required=True, min_length=2)
    last_name = serializers.CharField(required=True, min_length=2)
    mobile = serializers.IntegerField(
        required=False,
        min_value=5000000000,
        max_value=9999999999
    )
    role_id = serializers.CharField(required=True, min_length=6)

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        # fields = ( "id", "username", "password", )
        fields = ('id', 'password', 'email', 'first_name', 'last_name', 'mobile', 'role_id')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    @time_it
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile=validated_data.get('mobile', 9988776655),
            role_id=validated_data['role_id'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'is_active', 'role_id')


class UserUpdateRequestSerializer(serializers.ModelSerializer):
    """
    Test ser
    """
    # mobile = serializers.IntegerField(
    #     min_value=5000000000,
    #     max_value=9999999999
    # )
    # TODO PUT validations for update, like mobile number and all refer UserRegSerializer
    id = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    mobile = serializers.IntegerField(required=True,
        min_value=5000000000,
        max_value=9999999999)
    # is_active = serializers.BooleanField(required=False)
    
    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.first_name= validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()
        return instance


    class Meta:
        model=User
        fields=('id','first_name','last_name','mobile')




class clientserializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'mobile', 'access_token', 'sub_cluster',
            'is_verified', 'is_active', 'email', 'image_url'
        )










    # def update(self,instance,validated_data):
    #     data = self
    #     instance.save()
    #     print(data)
    #     return instance

    # 



