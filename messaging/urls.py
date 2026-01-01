from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('start/<int:resource_id>/', views.start_conversation, name='start_conversation'),
    path('chat/<int:pk>/', views.chat_detail, name='chat_detail'),
    path('send/<int:pk>/', views.send_message, name='send_message'),
]
