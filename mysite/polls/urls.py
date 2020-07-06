from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import create_question_and_choices, QuestionDeleteView

app_name = 'polls'
urlpatterns = [
    # path('', views.index, name='index'),
    #
    # path('<int:question_id>/', views.detail, name='detail'),
    #
    # path('<int:question_id>/results/', views.results, name='results'),
    #
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.IndexView.as_view(), name='polls-home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='polls/logout.html'), name='logout'),
    path('question/create/', create_question_and_choices, name='question-create'),
    path('question/<int:pk>/edit/', create_question_and_choices, name='question-edit'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    # path( 'url(r'^simpleemail/(?P<emailto>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/', 'sendSimpleEmail' , name = 'sendSimpleEmail'),)
]
