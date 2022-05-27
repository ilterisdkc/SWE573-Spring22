from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.learning_space_list_view, name="learning_space_list"),
    path("quizzes", views.index, name="index"),
    path("quiz/<int:myid>/", views.quiz, name="quiz"),
    path('quiz/<int:myid>/data/', views.quiz_data_view, name='quiz-data'),
    path('quiz/<int:myid>/save/', views.save_quiz_view, name='quiz-save'),
    
    path("signup/", views.Signup, name="signup"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("profile/", views.profile, name='user_profile'),

    path("search", views.search_learning_spaces, name='search_learning_spaces'),
    
    path('add_quiz/', views.add_quiz, name='add_quiz'),    
    path('add_question/', views.add_question, name='add_question'),  
    path('add_options/<int:myid>/', views.add_options, name='add_options'), 
    path('results/', views.results, name='results'),    
    path('delete_question/<int:myid>/', views.delete_question, name='delete_question'),  
    path('delete_result/<int:myid>/', views.delete_result, name='delete_result'),

    path('subject/<int:subject_id>', views.subject_view, name='subject'),
    path('subject_create/', views.SubjectCreateView.as_view(), name='create_subject'),
    path('subject_edit/<int:pk>', views.SubjectEditView.as_view(), name='edit_subject'),
    path('subject_list/', views.subject_list_view, name='subject_list'),
    path('delete_subject/<int:myid>', views.delete_subject, name='delete_subject'),

    path('learning_space_create/', views.CreateLearningSpace.as_view(), name='create_lerning_space'),
    path('learning_space_list/', views.learning_space_list_view, name='learning_space_list'),
    path('learning_space/<int:learning_space_id>', views.learning_space_view, name='learning_space'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)