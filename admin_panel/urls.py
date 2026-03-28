from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.manage_users, name='users'),
    path('emotions/', views.emotion_reports, name='emotions'),
    path('recommendations/', views.manage_recommendations, name='manage_recommendations'),
    path('feedback/', views.feedback_management, name='feedback'),
    path('analytics/', views.analytics_view, name='analytics'),
]
