"""
URL configuration for dream project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from interior import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Django Admin Panel
    path("admin/", admin.site.urls),
    
    # Core Public Facing Pages
    path('', views.index, name='index'),
    
    # Staff Authentication Pathways
    path('staff/', views.staff, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Secure Control Panel Layout
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Inventory CRUD Endpoints
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    
    # Customer Lead Generation CRUD Endpoints
    path('update-enquiry/<int:pk>/', views.update_enquiry, name='update_enquiry'),
    path('delete-enquiry/<int:pk>/', views.delete_enquiry, name='delete_enquiry'),
    path('add-gallery/', views.add_gallery_item, name='add_gallery_item'),
    path('delete-gallery/<int:pk>/', views.delete_gallery_item, name='delete_gallery_item'),
]

# Serve Uploaded Media Buffers locally on Local Development environments
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )