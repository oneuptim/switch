# -*- coding: utf-8 -*-
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser

# Import the basic Django ORM models library
from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime
from taggit.managers import TaggableManager



# Subclass AbstractUser
class User(AbstractUser):
    GENDER_CHOICES =(
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
    )

    profile_image = ProcessedImageField(
        upload_to='profile_image',
        processors=[ResizeToFill(560, 230)],
        format='JPEG',
        options={'quality': 90},
        blank=True,
    )
    telephone = models.CharField(
        max_length=15
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    bio = models.TextField()
    interest = TaggableManager()

    def __unicode__(self):
        return self.username

    @property
    def get_image_url(self):
        return self.prole_image.url


class QuestionsAndAnswers(models.Model):

    answer = models.CharField(
        max_length=140,
    )

    date_posted = models.DateTimeField(
        default=timezone.now
    )

    user = models.ForeignKey(
        User,
    )

    class Meta:
        abstract = True


class Question(QuestionsAndAnswers):
    pass


class Answer(QuestionsAndAnswers):
    pass


class Date(models.Model):
    woman = models.ForeignKey(User, related_name='woman')
    man = models.ForeignKey(User, related_name='man')
    date_added = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u"%s is dating %s" % (self.woman.username,
                                        self.man.username)

    def save(self, **kwargs):
        if self.woman == self.man:
            raise ValueError("Cannot Date Yourself")
        super(Date, self).save(**kwargs)

    class Meta:
        unique_together = (('woman', 'man'),)
