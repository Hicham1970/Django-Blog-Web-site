from django.contrib import admin
from .models import Blog, Category, Comment


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category',
                    'status', 'section', 'created_at')
    list_filter = ('status', 'section', 'category', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'blog_slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'parent')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'comment_text')
    readonly_fields = ('created_at',)
    raw_id_fields = ('post', 'parent')
    ordering = ('-created_at',)
