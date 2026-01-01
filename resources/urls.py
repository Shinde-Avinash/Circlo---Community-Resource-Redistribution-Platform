from django.urls import path
from . import views

urlpatterns = [
    path('<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('create/', views.post_resource, name='post_resource'),
    path('update/<int:resource_id>/', views.update_resource, name='update_resource'),
    path('delete/<int:resource_id>/', views.delete_resource, name='delete_resource'),
    path('claim/<int:resource_id>/', views.claim_resource, name='claim_resource'),
    path('unclaim/<int:resource_id>/', views.unclaim_resource, name='unclaim_resource'),
    # Force reload
]
