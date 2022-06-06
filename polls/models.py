import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import When, Case, Value
from django.utils import timezone


class AnnotationQuerySet(models.QuerySet):
    def do_annotation(self):
        now = timezone.now()
        return self.annotate(was_published_recently=Case(
            When(pub_date__gte=now - datetime.timedelta(days=1),
                 pub_date__lte=now, then=Value(True)),
            default=Value(False), output_field=models.BooleanField()
        )
        )


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')

    objects = AnnotationQuerySet.as_manager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


def validate_value(value):
    if value < 0:
        raise ValidationError('%(value)s is wrong',
                              params={'value': value}, )


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, validators=[validate_value])

    def __str__(self):
        return self.choice_text
