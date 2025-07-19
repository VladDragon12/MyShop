from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    list_filter = ['available', 'created', 'category']
    list_editable = ['price', 'stock', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug')
        }),
        (_('Pricing'), {
            'fields': ('price', 'stock', 'available')
        }),
        (_('Content'), {
            'fields': ('image', 'description')
        }),
        (_('Metadata'), {
            'fields': ('created', 'updated')
        }),
    )