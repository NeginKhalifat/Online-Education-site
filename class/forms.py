from django import forms
from .models import (
    Class, Team, Quiz, RecordMark, Question
)
from django import forms
from django.contrib.auth.models import User

from bootstrap3_datetime.widgets import DateTimePicker


class TeamRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)
        print(self.user)
        form_choices = User.objects.exclude(username__exact=self.user)

        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=form_choices, widget=forms.CheckboxSelectMultiple)

    #    self.members = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Team
        exclude = ['owner', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ClassRegistrationForm(forms.ModelForm):
    #
    duration = forms.TimeField(widget=DateTimePicker(options={"format": "HH:mm"}))
    date = forms.DateTimeField(
        required=False, widget=DateTimePicker(options={"format": "MM/DD/YYYY HH:mm"})
    )
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Class
        exclude = ['owner', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'date': DateTimePicker(),
            # 'duration': forms.TimeField(attrs={'class': 'form-control'}),

        }


class QuizCreatorForm(forms.ModelForm):
    duration = forms.TimeField(widget=DateTimePicker(options={"format": "HH:mm"}))
    date = forms.DateTimeField(
        required=False, widget=DateTimePicker(options={"format": "MM/DD/YYYY HH:mm"})
    )

    #  class_name=forms.ModelChoiceField(   queryset=Class.objects.all(), empty_label="Selected value")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QuizCreatorForm, self).__init__(*args, **kwargs)
        print(self.user)
        if self.user:
            form_choices = Class.objects.filter(owner=self.user)

            type_choices = [(choice.pk, choice) for choice in form_choices]
            print('tt', type_choices)
            # self.fields['class_name'] = forms.ChoiceField(choices=type_choices)
            print(form_choices.all())
            self.fields['class_name'].queryset = Class.objects.filter(owner=self.user).all()
        # forms.ModelChoiceField(
        # queryset=Class.objects.values_list('title', flat=True).filter(owner=self.user).distinct())

    class Meta:
        model = Quiz
        exclude = ['owner', 'slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuestionCreateForm(forms.ModelForm):
    value = forms.FloatField()

    class Meta:
        model = Question
        exclude = ['exam', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),

            'questions': forms.TextInput(attrs={'class': 'form-control'}),
            'option1': forms.TextInput(attrs={'class': 'form-control'}),
            'option2': forms.TextInput(attrs={'class': 'form-control'}),
            'option3': forms.TextInput(attrs={'class': 'form-control'}),
            'option4': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
        }
