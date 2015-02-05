__author__ = 'larry'
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Question, Answer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'gender',
            'profile_image',
            'age',
            'bio',
        )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer


class ProfileSerializer(serializers.ModelSerializer):
    # GENDER_CHOICES =(
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # )
    # profile_image = serializers.ImageField(
    #     max_length=None,
    #     allow_empty_file=False,
    #     use_url=True
    # )
    # profile_image = serializers.Field(source='get_image_url')
    gender = serializers.CharField( )
    class Meta:
        model = User
        fields = [
            'id',
            'gender',
            "bio",
            "age",
        ]

    # def get_image_url(self, obj):
    #     return User.profile_image.url


class DateSerializer(serializers.Serializer):
    man = serializers.IntegerField()