from django.contrib import admin
from .models import Enquiry,Product,GalleryItem


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "phone",
        "email",
        "project_type",
        "budget",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    list_filter = (
        "project_type",
        "budget",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'created_at'
    )

    list_filter = (
        'category',
        'created_at'
    )

    search_fields = (
        'name',
        'category'
    )

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'grid_class', 'order')
    list_editable = ('order', 'grid_class')