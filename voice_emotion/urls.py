from django.urls import path
from . import views

app_name = 'voice_emotion'

urlpatterns = [
    path('analyze/', views.analyze_view, name='analyze'),
    path('api/analyze/', views.analyze_emotion_api, name='analyze_api'),
    path('history/', views.history_view, name='history'),
]
