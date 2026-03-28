from django.urls import path
from . import views

app_name = 'user_dashboard'

urlpatterns = [
    path('', views.user_dashboard, name='dashboard'),
    path('emotions/', views.user_emotion_history, name='emotions'),
    path('recommendations/', views.user_recommendations, name='user_recommendations'),
    path('feedback/', views.user_feedback_history, name='user_feedback'),
]
