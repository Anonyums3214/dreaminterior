from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Enquiry, Product, GalleryItem

def index(request):
    if request.method == "POST":
        Enquiry.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            project_type=request.POST.get('project_type'),
            location=request.POST.get('location', 'Tezpur'), 
            budget=request.POST.get('budget'),
            message=request.POST.get('message'),
        )
        messages.success(request, "Your enquiry has been submitted successfully")
        return redirect('/')

    context = {
        # Dynamically inject the gallery assets configured via your dashboard/admin
        'gallery_items': GalleryItem.objects.all(),
        
        # Product queries matching the front-end tabs architecture
        'kitchen_products': Product.objects.filter(category__iexact='Kitchen'),
        'bedroom_products': Product.objects.filter(category__iexact='Bedroom'),
        'furniture_products': Product.objects.filter(category__iexact='Furniture'),
        'office_products': Product.objects.filter(category__iexact='Office Interior'),
        'wall_products': Product.objects.filter(category__iexact='Walls & Ceiling'),
        'lighting_products': Product.objects.filter(category__iexact='Lighting'),
    }
    return render(request, "index.html", context)


def staff(request):
    # If a logged-in superuser/staff tries to visit login page, send them straight to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')

    if request.method == "POST":
        user_val = request.POST.get('username', '').strip()
        pass_val = request.POST.get('password', '').strip()

        # Validate credentials against Django's auth user table
        user = authenticate(request, username=user_val, password=pass_val)

        if user is not None:
            if user.is_staff or user.is_superuser:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Access Denied: Restrictive account clearances.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'staff_access.html')


# Secure your backend dashboard so ordinary guests can't guess URLs and snoop files
@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Unauthorized access restricted.")
        return redirect('login')

    enquiries = Enquiry.objects.all()
    products = Product.objects.all()
    gallery_items = GalleryItem.objects.all()
    
    total_enquiries = enquiries.count()
    pending_leads = enquiries.filter(status='pending').count()
    total_products = products.count()

    context = {
        'enquiries': enquiries,
        'products': products,
        'gallery_items': gallery_items,
        'total_enquiries': total_enquiries,
        'pending_leads': pending_leads,
        'total_products': total_products,
    }
    return render(request, "dashboard.html", context)


def logout_view(request):
    auth_logout(request)
    messages.success(request, "Logged out securely.")
    return redirect('index')


# ═══════════════════════════════════════════════════
# INVENTORY CONTROL ENDPOINTS (CRUD)
# ═══════════════════════════════════════════════════
@login_required(login_url='login')
def add_product(request):
    if not request.user.is_staff: return redirect('login')
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            price=request.POST.get('price'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )
        messages.success(request, "Product added successfully")
    return redirect('dashboard')

@login_required(login_url='login')
def delete_product(request, pk):
    if not request.user.is_staff: return redirect('login')
    product = get_object_or_404(Product, id=pk)
    if product.image:
        product.image.delete()
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('dashboard')


# ═══════════════════════════════════════════════════
# PORTFOLIO/GALLERY CONTROL ENDPOINTS (CRUD)
# ═══════════════════════════════════════════════════
@login_required(login_url='login')
def add_gallery_item(request):
    if not request.user.is_staff: return redirect('login')
    if request.method == "POST":
        GalleryItem.objects.create(
            title=request.POST.get('title'),
            grid_class=request.POST.get('grid_class', 'g1'),
            order=request.POST.get('order', 0),
            image=request.FILES.get('image')
        )
        messages.success(request, "Gallery photo added successfully")
    return redirect('dashboard')

@login_required(login_url='login')
def delete_gallery_item(request, pk):
    if not request.user.is_staff: return redirect('login')
    item = get_object_or_404(GalleryItem, id=pk)
    if item.image:
        item.image.delete()
    item.delete()
    messages.success(request, "Gallery photo removed successfully")
    return redirect('dashboard')


# ═══════════════════════════════════════════════════
# ENQUIRY/LEAD MANAGEMENT ENDPOINTS
# ═══════════════════════════════════════════════════
@login_required(login_url='login')
def update_enquiry(request, pk):
    if not request.user.is_staff: return redirect('login')
    if request.method == "POST":
        enquiry = get_object_or_404(Enquiry, id=pk)
        enquiry.status = request.POST.get('status')
        enquiry.save()
        messages.success(request, "Enquiry status updated successfully")
    return redirect('dashboard')

@login_required(login_url='login')
def delete_enquiry(request, pk):
    if not request.user.is_staff: return redirect('login')
    enquiry = get_object_or_404(Enquiry, id=pk)
    enquiry.delete()
    messages.success(request, "Enquiry record deleted successfully")
    return redirect('dashboard')