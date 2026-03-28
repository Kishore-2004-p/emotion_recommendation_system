from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendations_list, name='list'),
    path('history/', views.recommendation_history, name='history'),
    path('<int:item_id>/feedback/', views.feedback_view, name='feedback'),
]
