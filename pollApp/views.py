from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'pollApp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollApp/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollApp/results.html'



# def index(request):
#     latest_question_text = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_text': latest_question_text}
#     return render(request,'pollApp/index.html',context)
#
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'pollApp/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,'pollApp/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('pollApp:results', args=(question.id,)))
