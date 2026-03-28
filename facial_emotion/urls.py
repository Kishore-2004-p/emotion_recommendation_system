from django.urls import path
from . import views

app_name = 'facial_emotion'

urlpatterns = [
    path('detect/', views.detect_view, name='detect'),
    path('history/', views.history_view, name='history'),
    path('api/detect/', views.detect_emotion_api, name='detect_api'),  # Add this
]
