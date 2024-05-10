from django.contrib import admin

from .models import Category, Location, Post


admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_files = ('title', )
    list_display = ('id', 'title', 'description', 'slug',
                    'is_published', 'created_at')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    list_filter = ('created_at', )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_files = ('name', )
    list_display = ('id', 'name', 'is_published', 'created_at')
    list_display_links = ('name', )
    list_editable = ('is_published', )
    list_filter = ('created_at', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_files = ('text', )
    list_display = ('id', 'title', 'author', 'text', 'category',
                    'pub_date', 'location', 'is_published', 'created_at')
    list_display_links = ('title', )
    list_editable = ('category', 'is_published', 'location')
    list_filter = ('created_at', )
