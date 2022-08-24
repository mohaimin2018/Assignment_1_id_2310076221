from django.http import Http404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question

###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
The home() function will return the home.html page on the localhost server page
"""

def home(request):
    return render(request, 'polls/home.html')


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
In detail() function, if the question does not exist in the database then an issue can be generated.
To handel the issue, DoesNotExist Exception is thrown here. Otherwise, the function will return the
detail.html page.
"""

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Here the results() function will return the question id and the results.html page, if the question
is existed, otherwise, it will return 404(Page Not Found).
"""

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Here the vote() function will return the text with the question id which is written
in the HttpResponse() function.
"""

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Here the index() function will return the index.html page with the question list which is ordered
according to the publishing date.
"""

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Here the vote() function will handel the DoesNotExist exception. If anyone does not select 
any choice then the function will return an error message and if the choice is selected then
the vote will be counted and increased and it will be returned to the result.html page.
"""

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
The class IndexView is a generic view which is helping to generate list and detail view of object.
The class demands a template name and a object list. The get_queryset() function will return a set
of object according to the publishing date.
"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
The class DetailView is a generic view which is helping to generate list and detail view of object.
The class demands a model and a template name.The get_queryset() function will return a set
of object according to the publishing date.
"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):

        return Question.objects.filter(pub_date__lte=timezone.now())


###############################################################################################################


"""
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<------COMMENT------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
The class ResultsView is a generic view which is helping to generate list and detail view of object.
The class demands a model and a template name.
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


###############################################################################################################