import logging
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .models import Question, Choice

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    """ Returns last 5 published questions """

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def validate_value(value):
    if value<0:
        raise ValidationError(_('%(value)s is wrong'),
            params={'value': value},)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError) as exc:
        logger.error(exc)
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    except (Choice.DoesNotExist) as exc:
        logger.error(exc)
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Incorrect choice",
        })
    else:
        validate_value(selected_choice)
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return redirect('polls:result', pk=question_id)
