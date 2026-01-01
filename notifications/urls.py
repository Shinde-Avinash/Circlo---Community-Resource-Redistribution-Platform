from django.urls import path
from . import views

urlpatterns = [
    path('count/', views.unread_count, name='notification_count'),
    path('list/', views.notification_list, name='notification_list'),
    path('read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('clear/', views.clear_all, name='clear_notifications'),
]
