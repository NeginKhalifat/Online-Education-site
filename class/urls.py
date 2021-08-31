from django.urls import path, include, re_path
from .views import AddClass, class_registration, class_list, team_registration, ClassesView, TeamView, member_list, \
    MemberView, student_list,create_quiz,QuizView,add_question,quiz_list,question_list

app_name = 'class'

urlpatterns = [
    path('addclass/', class_registration, name='create_class'),
    path('classlist/', ClassesView.as_view(), name='class_list'),

    path('classlist/<slug>/studentlist', student_list, name='student_list'),
    path('teamlist/', TeamView.as_view(), name='team_list'),
    path('teamlist/<slug>/memberlist', MemberView.as_view(), name='member_list'),
    path('createquiz/', create_quiz, name='create_quiz'),
    path('createquiz/<slug>/addquestions/<int:p>', add_question, name='add_question'),
    path('quizlist/', quiz_list, name='quiz_list'),
path('quizlist/<slug>/questionlist', question_list, name='question_list'),
    # path(r'^(?P<slug>[\w-]+)/memberslist', member_list, name='member_list'),

    # path(r'^(?P<slug>[\w-]+)/$', ClassesView.as_view(), name='class_view'),
    path('addteam/', team_registration, name='create_team'),

    # path('addquiz',)
]
