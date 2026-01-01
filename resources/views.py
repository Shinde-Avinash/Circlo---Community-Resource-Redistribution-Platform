from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resource, Claim
from .forms import ResourceForm

@login_required
def post_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.donor = request.user
            # Use user's location if not provided in form (fallback)
            if not resource.latitude and request.user.latitude:
                resource.latitude = request.user.latitude
                resource.longitude = request.user.longitude
            
            # If still no location, default to Pune for demo
            if not resource.latitude:
                 resource.latitude = 18.5204
                 resource.longitude = 73.8567

            resource.save()
            messages.success(request, "Resource posted successfully!")
            return redirect('home')
    else:
        form = ResourceForm()
    
    # Fetch user's history
    posted_resources = Resource.objects.filter(donor=request.user).order_by('-created_at')
    
    # Updated: Claimed resources now come from the Claim model
    from .models import Claim
    my_claims = Claim.objects.filter(claimant=request.user).order_by('-claimed_at')

    return render(request, 'resources/post_resource.html', {
        'form': form, 
        'title': 'Post a Resource',
        'posted_resources': posted_resources,
        'my_claims': my_claims
    })

@login_required
def update_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    # Check permission: Owner OR Moderator OR Superuser
    is_moderator = request.user.role == 'moderator' or request.user.is_superuser
    if resource.donor != request.user and not is_moderator:
        messages.error(request, "You are not authorized to edit this resource.")
        return redirect('resource_detail', resource_id=resource.id)

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully!")
            return redirect('update_resource', resource_id=resource.id)
    else:
        form = ResourceForm(instance=resource)
    
    # Fetch user's history for sidebar
    posted_resources = Resource.objects.filter(donor=request.user).order_by('-created_at')
    my_claims = Claim.objects.filter(claimant=request.user).order_by('-claimed_at')
    
    return render(request, 'resources/post_resource.html', {
        'form': form, 
        'title': 'Edit Resource',
        'posted_resources': posted_resources,
        'my_claims': my_claims
    })

def verify_claim(request, token):
    try:
        claim = Claim.objects.get(verification_token=token)
        
        # Ensure only the donor can verify (or maybe just allow open verification if the URL is secret? 
        # Ideally, donor should be logged in, but for ease of use at pickup, open link might be okay if token is high entropy UUID.
        # But let's check for donor authentication for security if possible, OR show a confirmation page for the donor to click "Confirm".
        # SIMPLIFIED FOR DEMO: If user is logged in and is donor -> verify. Else show info.
        
        if request.user.is_authenticated and request.user == claim.resource.donor:
            if not claim.is_verified:
                claim.is_verified = True
                claim.verified_at = timezone.now()
                claim.save()
                messages.success(request, f"Successfully verified claim for {claim.resource.title}!")
            else:
                messages.info(request, "This claim has already been verified.")
        elif not request.user.is_authenticated:
             # Redirect to login with next param
             return redirect(f'/accounts/login/?next={request.path}')
        else:
             messages.error(request, "You are not authorized to verify this claim.")
             return redirect('home')
             
        return redirect('dashboard')
        
    except Claim.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect('home')

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    # Check permission
    is_moderator = request.user.role == 'moderator' or request.user.is_superuser
    if resource.donor != request.user and not is_moderator:
        messages.error(request, "You are not authorized to delete this resource.")
        return redirect('resource_detail', resource_id=resource.id)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, "Resource deleted successfully.")
        return redirect('home')
    return redirect('resource_detail', resource_id=resource.id)

def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    return render(request, 'resources/detail.html', {'resource': resource})

@login_required
def claim_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    from .models import Claim

    if request.method == 'POST':
        if not resource.is_active:
            messages.error(request, "This resource is no longer active.")
            return redirect('home')
        
        try:
            claim_qty = int(request.POST.get('quantity', 1))
        except ValueError:
            claim_qty = 1
            
        if claim_qty <= 0:
            messages.error(request, "Quantity must be at least 1.")
            return redirect('resource_detail', resource_id=resource_id)

        if claim_qty > resource.available_quantity:
            messages.error(request, f"Review error: Only {resource.available_quantity} available.")
            return redirect('resource_detail', resource_id=resource_id)
        
        # Create Claim Record
        Claim.objects.create(
            resource=resource,
            claimant=request.user,
            quantity=claim_qty
        )
        
        # Decrement Inventory
        resource.available_quantity -= claim_qty
        if resource.available_quantity == 0:
            resource.is_active = False # Mark inactive if fully claimed
        resource.save()

        messages.success(request, f"Successfully claimed {claim_qty} {resource.unit} of {resource.title}.")
        return redirect('home')
    
    return render(request, 'resources/claim_confirm.html', {'resource': resource})

@login_required
def unclaim_resource(request, resource_id):
    # This ID acts as Claim ID or Resource ID fallback. 
    # NOTE: The URL parameter name is `resource_id`, but in partial claim system, 
    # we usually need the Claim ID to unclaim a SPECIFIC claim.
    # However, to keep it simple and compatible, we'll try to find the USER's claim for this resource.
    
    resource = get_object_or_404(Resource, id=resource_id)
    from .models import Claim
    
    # Find the most recent claim by this user for this resource
    user_claim = Claim.objects.filter(resource=resource, claimant=request.user).first()
    
    if not user_claim:
        messages.error(request, "You confirm you haven't claimed this resource (or already unclaimed it).")
        return redirect('post_resource')
    
    if request.method == 'POST':
        # Restock inventory
        resource.available_quantity += user_claim.quantity
        resource.is_active = True # Reactivate if it was closed
        resource.save()
        
        # Delete claim record
        qty_restored = user_claim.quantity
        user_claim.delete()
        
        messages.success(request, f"Unclaimed successfully. {qty_restored} {resource.unit} added back.")
        return redirect('post_resource')
    
    return redirect('home')
