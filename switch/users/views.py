# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse

# view imports
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views.generic import ListView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from rest_framework import viewsets
from .forms import UserForm

# Import the customized User model
import models
from rest_framework import viewsets,status
import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.parsers import FileUploadParser
from django.core.exceptions import ObjectDoesNotExist



class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm

    # we already imported User in the view code above, remember?
    model = models.User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return models.User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = models.User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    model = models.User
    parser_classes = (FileUploadParser,)


    @detail_route(methods=['post'])
    def profile(self, request, pk=None):
        api_user = self.get_object()
        serializer = serializers.ProfileSerializer(data=request.DATA, partial=True)
        # file_obj = request.FILES['profile_image']
        # print file_obj
        if serializer.is_valid():
            api_user.age = serializer.data['age']
            api_user.bio = serializer.data['bio']
            api_user.gender = serializer.data['gender']
            print serializer.data['gender']
            # # api_user.profile_image = file_obj
            api_user.save()
            print type(api_user)
            user_serialized = serializers.ProfileSerializer(api_user)
            return Response(user_serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def date(self, request, pk=None):
        api_user = self.get_object()
        serializer = serializers.DateSerializer(data=request.DATA)

        if serializer.is_valid():
            try:
                user_man = models.User.objects.get(id=serializer.data['man'])
            except ObjectDoesNotExist:
                return Response({"message":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

            models.Date.objects.create(
                woman=api_user,
                man=user_man,
            )

            return Response({"number":user_man.telephone}, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    # def post_save(self, user, *args, **kwargs):
    #     if type(user.interest) is list:
    #         saved_interest = models.User.objects.get(pk=user.pk)
    #         for tag in user.interest:
    #             saved_interest.interest.add(tag)




class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all()
    model = models.Question


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()
    model = models.Answer


class GirlViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(gender="F")
    model = models.User
