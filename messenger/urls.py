from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='messenger_inbox'),
    path('compose/', views.compose, name='messenger_compose'),
    path('<int:pk>/', views.message_detail, name='messenger_detail'),
]