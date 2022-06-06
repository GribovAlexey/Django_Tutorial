import logging

from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from .models import Question, Choice

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def redirect_to_index(self):
    return redirect('polls:index')


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
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return redirect('polls:result', pk=question_id)
