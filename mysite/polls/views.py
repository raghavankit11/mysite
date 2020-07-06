from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden

from .models import Question, Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, QuestionForm, ChoiceForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserRegisterForm()
    return render(request, 'polls/register.html', {'form': form})

class IndexView(generic.ListView):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # # output = ', '.join([q.question_text for q in latest_question_list])
    # context = {'latestposts': latest_question_list}
    # return render(request, 'polls/index.html', context)

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'      # for ListView, the automatically generated context variable is question_list.

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class DetailView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question':question})

    model = Question
    template_name = 'polls/detail.html'


    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
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

# class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
#     model = Question
#     fields = ['question_text', 'pub_date']
#
#
#     def form_valid(self, form):
#         form.instance.questioner = self.request.user
#         return super().form_valid(form)




@login_required()
def create_question_and_choices_single_choice(request, pk=None):

    q_obj = Question.objects.get(id=pk) if pk else Question()
    if pk is None or q_obj.questioner == request.user:
        c_obj = q_obj.choices.first() if pk else Choice()
        if request.method == 'POST':
            q_form = QuestionForm(data=request.POST, instance=q_obj)
            c_form = ChoiceForm(data=request.POST, instance=c_obj)
            if q_form.is_valid() and c_form.is_valid():
                q_obj = q_form.save(commit=False)
                q_obj.questioner = request.user
                q_obj.save()

                c_obj = c_form.save(commit=False)
                c_obj.question = q_obj
                c_obj.save()
                return redirect('polls:polls-home')
        else:
            q_form = QuestionForm(instance=q_obj)
            c_form = ChoiceForm(instance=c_obj)

        context = {
            'q_form': q_form,
            'c_form': c_form}
        return render(request, 'polls/question_form.html', context)
    else:
        # return HttpResponseForbidden()
        raise PermissionDenied



from django.forms import formset_factory, inlineformset_factory
@login_required()
def create_question_and_choices(request, pk=None):
    q_obj = Question.objects.get(id=pk) if pk else Question()
    if pk is None or q_obj.questioner == request.user:
        ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), extra=0 if pk else 1)

        if request.method == 'POST':
            q_form = QuestionForm(data=request.POST, instance=q_obj)
            c_forms = ChoiceFormSet(request.POST, instance=q_obj)

            if q_form.is_valid() and c_forms.is_valid():
                q_obj = q_form.save(commit=False)
                q_obj.questioner = request.user
                q_obj.save()

                # c_objs = c_forms.save(commit=False)
                for c_form in c_forms:
                    c_obj = c_form.save(commit=False)
                    c_obj.question = q_obj
                    c_obj.save()
                return redirect('polls:polls-home')
        else:
            q_form = QuestionForm(instance=q_obj)
            c_forms = ChoiceFormSet(instance=q_obj if pk else None)

        context = {
            'q_form': q_form,
            'c_forms': c_forms}
        return render(request, 'polls/question_form.html', context)
    else:
        # return HttpResponseForbidden()
        raise PermissionDenied


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Question
    success_url = '/'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.questioner:
            return True
        return False