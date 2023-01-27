from accounts.models import Userdata
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
  
  password = serializers.CharField(label='비밀번호', write_only = True, style={'input_type': 'password'})
  password_confirm = serializers.CharField(label='비밀번호 확인', write_only = True, style={'input_type': 'password'})
  experience = serializers.ChoiceField(choices=Userdata.EXP_CHOICES)
  def create(self, validated_data):
    # password = validated_data['password']
    # password_confirm = validated_data['password_confirm']
    # if password != password_confirm:
    #   raise serializers.ValidationError({'password_confirm':'비밀번호가 일치하지 않습니다.'})
    # serializer = UserSerializer(data=validated_data)
    user = Userdata.objects.create_user(
      mail = validated_data['mail'],
      userid = validated_data['userid'],
      user_name = validated_data['user_name'],
      password = validated_data['password'],
      date_of_birth = validated_data['date_of_birth'],
      experience = validated_data['experience']
    )

    return user

  def validate_password(self, value):
    if len(value) < 8:
      raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
    return value

  def validate_password_confirm(self, value):
    if len(value) < 8:
      raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
    return value
  
  def validate(self, data):
    if data['password'] != data['password_confirm']:
      raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
    return data
 
  class Meta:
    model = Userdata
    fields = ['userid', 'mail', 'user_name', 'password', 'password_confirm', 'date_of_birth', 'experience']
    validators = [
      UniqueTogetherValidator(
        queryset=Userdata.objects.all(),
        fields=['userid', 'mail']
      )
    ]

class UserProfileSerializer(serializers.ModelSerializer):

  old_password = serializers.CharField(label='비밀번호', write_only = True, style={'input_type': 'password'})
  new_password = serializers.CharField(label='비밀번호 확인', write_only = True, style={'input_type': 'password'})
  new_password_confirm = serializers.CharField(label='비밀번호 확인', write_only = True, style={'input_type': 'password'})
  
  
  def validate_new_password(self, value):
    if len(value) < 8:
      raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
    return value

  def validate_new_password_confirm(self, value):
    if len(value) < 8:
      raise serializers.ValidationError("비밀번호는 8자 이상이어야 합니다.")
    return value

  def validate(self, data):
    if data['new_password'] != data['new_password_confirm']:
      raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
    return data

  class Meta:
    model = Userdata
    fields = ['mail', 'user_name', 'old_password', 'new_password', 'new_password_confirm', 'experience']
    validators = [
      UniqueTogetherValidator(
        queryset=Userdata.objects.all(),
        fields=['mail']
      )
    ]
