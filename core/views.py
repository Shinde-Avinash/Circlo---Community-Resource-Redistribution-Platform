from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from resources.models import Resource
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def home(request):
    resources = Resource.objects.filter(is_active=True).order_by('-created_at')
    
    # Search and Filtering
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    type_filter = request.GET.get('type', 'offer') # Default to 'offer'
    
    if type_filter:
        resources = resources.filter(resource_type=type_filter)
    
    if search_query:
        from django.db.models import Q
        resources = resources.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    if category_filter:
        resources = resources.filter(category=category_filter)
    
    # If user is not logged in, show all resources without distance filtering
    if not request.user.is_authenticated:
        # Just sort by urgency and recency
        urgency_map = {'red': 1, 'yellow': 2, 'green': 3}
        # Convert queryset to list to map urgency for sorting, or order by urgency field if it was integer
        # Since urgency is char, we can't easily sort by custom order in DB without Case/When
        # For simplicity, let's keep list sorting
        resources_list = list(resources)
        resources_list.sort(key=lambda x: urgency_map.get(x.urgency, 3))
        
        # Serialize for map (Authentication not required for basic map)
        map_resources = []
        for res in resources_list:
             map_resources.append({
                'id': res.id,
                'title': res.title,
                'latitude': res.latitude,
                'longitude': res.longitude,
                'category': res.category,
                'urgency': res.urgency,
                'available_quantity': res.available_quantity,
                'unit': res.unit,
                'url': f"/resources/{res.id}/", 
            })
            
        return render(request, 'home.html', {'resources': resources_list, 'map_resources': map_resources})

    # User is logged in, apply location filtering
    user_lat = request.user.latitude if request.user.latitude else 18.5204
    user_long = request.user.longitude if request.user.longitude else 73.8567
        
    nearby_resources = []
    for res in resources:
        dist = haversine(user_long, user_lat, res.longitude, res.latitude)
        res.distance_km = round(dist, 1)
        # Filter for basic proximity (e.g., 50km for demo visibility, real app 10km)
        if dist <= 50: 
            nearby_resources.append(res)
            
    # Sort by urgency (custom sort) then distance
    urgency_map = {'red': 1, 'yellow': 2, 'green': 3}
    nearby_resources.sort(key=lambda x: (urgency_map.get(x.urgency, 3), x.distance_km))

    # If Search or Filter is active, pass flat list
    if search_query or category_filter:
        map_resources = []
        for res in nearby_resources:
            map_resources.append({
                'id': res.id,
                'title': res.title,
                'latitude': res.latitude,
                'longitude': res.longitude,
                'category': res.category,
                'urgency': res.urgency,
                'available_quantity': res.available_quantity,
                'unit': res.unit,
                'url': f"/resources/{res.id}/",
            })
        return render(request, 'home.html', {'resources': nearby_resources, 'map_resources': map_resources})

    # Otherwise, group by category for "Netflix-style" section display
    # Preferred Order: Food -> Clothing -> Supplies -> Furniture -> Books -> Other
    display_order = ['food', 'clothing', 'supplies', 'furniture', 'books', 'other']
    categorized_resources = []
    
    for cat in display_order:
        # Filter matching resources for this category
        items = [r for r in nearby_resources if r.category == cat]
        if items:
            categorized_resources.append({
                'name': cat,
                'items': items
            })
            
    # Add any remaining categories not in our preferred list (fallback)
    known_cats = set(display_order)
    other_items = [r for r in nearby_resources if r.category not in known_cats]
    if other_items:
        categorized_resources.append({'name': 'Others', 'items': other_items})

    # Serialize resources for the map
    map_resources = []
    # Use nearby_resources if logged in, otherwise use all visible resources (resources_list)
    # Note: access `resources_list` if user not authenticated
    
    target_list = nearby_resources if request.user.is_authenticated else resources_list
    
    for res in target_list:
        map_resources.append({
            'id': res.id,
            'title': res.title,
            'latitude': res.latitude,
            'longitude': res.longitude,
            'category': res.category,
            'urgency': res.urgency,
            'available_quantity': res.available_quantity,
            'unit': res.unit,
            'url': f"/resources/{res.id}/", # Hardcoding url path to avoid reverse complexity in loop, or could use reverse
        })

    return render(request, 'home.html', {
        'categorized_resources': categorized_resources,
        'resources': nearby_resources,
        'map_resources': map_resources
    })

@login_required
def dashboard(request):
    # Admin/Moderator Check
    if not (request.user.role == 'moderator' or request.user.is_superuser):
        messages.error(request, "Access Denied: Admins only.")
        return redirect('home')

    total_posted = Resource.objects.count()
    total_active = Resource.objects.filter(is_active=True).count()
    total_claimed = Resource.objects.filter(is_active=False).count()
    
    # Calculate claim rate
    pending_ratio = 0
    if total_posted > 0:
        pending_ratio = round((total_claimed / total_posted) * 100, 1)

    # Urgency Stats
    urgency_counts = {
        'red': Resource.objects.filter(urgency='red').count(),
        'yellow': Resource.objects.filter(urgency='yellow').count(),
        'green': Resource.objects.filter(urgency='green').count(),
    }

    # Category Stats
    from django.db.models import Count
    cat_stats = Resource.objects.values('category').annotate(count=Count('category'))
    category_labels = [c['category'] for c in cat_stats]
    category_counts = [c['count'] for c in cat_stats]

    # Recent Activity
    recent_resources = Resource.objects.all().order_by('-created_at')[:5]
    
    # User Stats (Lazy import or move to users app ideally, but here for dashboard)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    total_users = User.objects.count()
    recent_users = User.objects.all().order_by('-date_joined')[:5]

    context = {
        'total_posted': total_posted,
        'total_active': total_active,
        'total_claimed': total_claimed,
        'pending_ratio': pending_ratio,
        'urgency_counts': urgency_counts,
        'category_labels': category_labels,
        'category_counts': category_counts,
        'recent_resources': recent_resources,
        'total_users': total_users,
        'recent_users': recent_users,
    }
    return render(request, 'dashboard.html', context)

def leaderboard(request):
    from django.db.models import Count
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Aggregate resources count per user
    top_donors = User.objects.annotate(resource_count=Count('resources')).filter(resource_count__gt=0).order_by('-resource_count')[:20]
    
    # Process badges
    ranked_donors = []
    for index, donor in enumerate(top_donors):
        rank = index + 1
        badge = None
        if rank == 1:
            badge = '🥇 Gold Donor'
        elif rank == 2:
            badge = '🥈 Silver Donor'
        elif rank == 3:
            badge = '🥉 Bronze Donor'
        elif donor.resource_count >= 5:
            badge = '🌟 Sustainability Champion'
        elif donor.resource_count >= 1:
            badge = '✅ Verified'
            
        ranked_donors.append({
            'rank': rank,
            'user': donor,
            'count': donor.resource_count,
            'badge': badge
        })
        
    return render(request, 'leaderboard.html', {'ranked_donors': ranked_donors})

from django.views.decorators.cache import cache_control

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def service_worker(request):
    return render(request, 'sw.js', content_type='application/javascript')
