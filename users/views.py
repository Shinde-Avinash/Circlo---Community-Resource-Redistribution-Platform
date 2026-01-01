from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserUpdateForm, AdminUserEditForm
from .models import User

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Circlo, {user.username}!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

# Redirect old admin_dashboard to new dashboard or just keep as entry?
# Let's redirect /users/admin-panel to the core dashboard for central access
@login_required
def admin_dashboard(request):
   return redirect('dashboard')

@login_required
def manage_users(request):
    if not (request.user.role == 'moderator' or request.user.is_superuser):
        messages.error(request, "Access Denied.")
        return redirect('home')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/manage_users.html', {'users': users})

@login_required
def manage_resources(request):
    from resources.models import Resource, Claim
    if request.user.is_superuser or request.user.role == 'moderator':
        resources = Resource.objects.all().order_by('-created_at')
    else:
        resources = Resource.objects.filter(donor=request.user).order_by('-created_at')
    
    # Use prefetch_related if needed, but for now simple filter
    claims = Claim.objects.filter(claimant=request.user).select_related('resource', 'resource__donor').order_by('-claimed_at')
    
    return render(request, 'users/manage_resources.html', {'resources': resources, 'claims': claims})

@login_required
def delete_user(request, user_id):
    if not (request.user.role == 'moderator' or request.user.is_superuser):
        messages.error(request, "Access Denied.")
        return redirect('home')
    
    user_to_delete = get_object_or_404(User, id=user_id)
    # Prevent self-deletion
    if user_to_delete == request.user:
        messages.error(request, "You cannot delete your own account here.")
    else:
        user_to_delete.delete()
        messages.success(request, "User deleted successfully.")
    
    return redirect('manage_users')

@login_required
def edit_user(request, user_id):
    if not (request.user.role == 'moderator' or request.user.is_superuser):
        messages.error(request, "Access Denied.")
        return redirect('home')
        
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user_to_edit.username} updated successfully.")
            return redirect('edit_user', user_id=user_to_edit.id)
    else:
        form = AdminUserEditForm(instance=user_to_edit)
    
    return render(request, 'users/edit_user_admin.html', {'form': form, 'user_to_edit': user_to_edit})
