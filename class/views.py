from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import (
    Class, Team, Question, Quiz, RecordMark
)
from django.views.generic import (
    DetailView,
    View,
    ListView,
    CreateView,
    FormView,
    UpdateView,
    TemplateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import ClassRegistrationForm, TeamRegistrationForm, QuizCreatorForm, QuestionCreateForm
from django.core.paginator import Paginator


@login_required
def class_list():
    return


@login_required
def class_registration(request):
    forms = ClassRegistrationForm()
    print(request.user)
    if request.method == 'POST':
        forms = ClassRegistrationForm(request.POST)
        if forms.is_valid():
            instance = forms.save(commit=False)
            print(instance)
            instance.owner = request.user

            instance.save()
            forms.save_m2m()
            return redirect('class:class_list')
    context = {'forms': forms}
    return render(request, 'class/addclass.html', context)


@login_required
def team_registration(request):
    forms = TeamRegistrationForm(user=request.user)
    if request.method == 'POST':
        forms = TeamRegistrationForm(request.POST, request.user)
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.owner = request.user
            instance.save()
            forms.save_m2m()
            return redirect('class:team_list')

    context = {'forms': forms}
    return render(request, 'class/addteam.html', context)


class AddClass(LoginRequiredMixin, CreateView):
    queryset = Class.objects.all()
    template_name = 'class/addclass.html'
    context_object_name = 'classes'
    login_url = 'accounts:login'
    form_class = ClassRegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(AddClass, self).get_context_data(*args, **kwargs)
        # print(context)
        # print(self.request.path)
        # print(kwargs)
        # I used Detail view inheritance to grab the slug and be able to add it to the context. Since in create view It won't get it
        # I could also use request.path to grab the slug manually
        # and also, since I'll have to do the post manually, I'll have to get slug as a prameter
        # and if I were to set the get function manually as well, I did not have to use Detaiview since I could grab it as a prameter
        return context

    def post(self, request, *args, **kwargs):
        forms = ClassRegistrationForm(request.POST)
        print('hiiiiiiii')
        if forms.is_valid():
            print('valid')
            # forms.save()
            return redirect('class-list')

        context = {'forms': forms}
        return render(request, 'class/class-registration.html', context)


class DteailView(DetailView):
    queryset = Class.objects.all()
    template_name = 'Meeting/detail.html'
    context_object_name = 'classes'


class ClassesView(ListView):
    model = Class
    # queryset = word.objects.all().order_by('-date')
    template_name = 'class/listclass.html'
    context_object_name = 'register_class'
    paginate_by = 9

    def get_queryset(self):
        if self.request.GET.get('q'):
            queryset = Class.objects.search(self.request.GET.get('q'))
        else:
            queryset = Class.objects.all()
        return queryset


class MemberView(ListView):
    model = User
    # queryset =  set(User.objects.filter(team__slug=slug))
    template_name = 'class/listmember.html'
    context_object_name = 'members'
    paginate_by = 9

    def get_queryset(self, request, slug):
        q = Team.objects.filter(slug=slug, owner=request.user)
        queryset = q[0].members.all()
        return queryset


def member_list(request, slug):
    q = Team.objects.filter(slug=slug, owner=request.user)
    context = {'members': q[0].members.all()}
    return render(request, 'class/listmember.html', context)


def student_list(request, slug):
    classes = Class.objects.filter(slug=slug, owner=request.user)
    students = []
    for i in classes[0].teams.all():
        teams = Team.objects.filter(slug=slug)
        students += list(teams[0].members.all())

    context = {'students': list(set(students))}
    return render(request, 'class/liststudent.html', context)


class TeamView(ListView):
    model = Team
    # queryset = word.objects.all().order_by('-date')
    template_name = 'class/listteam.html'
    context_object_name = 'register_team'
    paginate_by = 9

    def get_queryset(self):

        if self.request.GET.get('q'):
            queryset = Team.objects.search(self.request.GET.get('q'))
        else:
            queryset = Team.objects.all()
        return queryset


@login_required()
def add_question(request, slug,p):
    forms = QuestionCreateForm()
    if request.method == 'POST':
        forms = QuestionCreateForm(request.POST)
        if forms.is_valid():
            instance = forms.save(commit=False)
            print(slug)
            quiz_name = Quiz.objects.filter(slug=slug).first()
            print(quiz_name)
            instance.exam = quiz_name
            instance.save()
            print(Question.objects.all())
            len_question = len(Question.objects.filter(exam=quiz_name.id))
            print(len_question)
            if 'add' in request.POST:
                return redirect('/createquiz/' + str(quiz_name.slug) + '/addquestions/' + str(p+1))
            elif 'done' in request.POST:
                return redirect('class:quiz_list')

    context = {'forms': forms}
    return render(request, 'class/addquestion.html', context)


@login_required()
def create_quiz(request):
    forms = QuizCreatorForm(user=request.user)
    if request.method == 'POST':
        forms = QuizCreatorForm(request.POST, request.user)
        if forms.is_valid():
            instance = forms.save(commit=False)
            instance.owner = request.user
            instance.save()
            len_question = len(Question.objects.filter(exam=instance.id))
            if 'add' in request.POST:
                print('hhhhhhhhhhhh')
                return redirect('/creatquiz/' + str(instance.slug) + '/addquestion/' + str(len_question + 1))
            elif 'done' in request.POST:
                return redirect('class:quiz_list')

    context = {'forms': forms}
    return render(request, 'class/createquiz.html', context)


class QuizView(ListView):
    model = Quiz
    # queryset = word.objects.all().order_by('-date')
    template_name = 'class/listquiz.html'
    context_object_name = 'quizes'
    paginate_by = 9

    def get_queryset(self):

        if self.request.GET.get('q'):
            queryset = Quiz.objects.search(self.request.GET.get('q'))
        else:
            queryset = Quiz.objects.all()
        return queryset

def quiz_list(request):
    q = Quiz.objects.filter( owner=request.user).all()
    context = {'quizes': q.all()}
    return render(request, 'class/listquiz.html', context)
def question_list(request,slug):
    q = Question.objects.filter( owner=request.user,slug=slug).all()
    context = {'questions': q.all()}
    return render(request, 'class/listquestion.html', context)
