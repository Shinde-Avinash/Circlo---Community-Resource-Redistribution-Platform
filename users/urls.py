from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'), # Kept for backward compat/redirect
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('manage/resources/', views.manage_resources, name='manage_resources'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
