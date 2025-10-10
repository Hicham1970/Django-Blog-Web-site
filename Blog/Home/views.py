from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.

def home(request):
    # Fetch all blog posts ordered by ID in desc. order
    post = Blog.objects.order_by('-id')
    # Assuming you have a boolean field 'main_post' in your Blog model
    main_post = Blog.objects.filter(main_post=True).order_by(
        '-id')[:1]  # Fetch the main post
    recent = Blog.objects.filter(section='Recent').order_by(
        '-id')[0:5]  # Fetch 5 recent posts
    popular = Blog.objects.filter(section='Popular').order_by(
        '-id')[0:5]  # Fetch 5 popular posts
    category = Category.objects.all()  # Fetch all categories
    context = {
        'post': post,
        'main_post': main_post,
        'recent': recent,
        'popular': popular,
        'category': category,
    }

    return render(request, 'index.html', context)


def blog_details(request, slug):
    # posts = Blog.objects.order_by('-id') # Fetch all blog posts ordered by ID in descending order
    category = Category.objects.all()  # Fetch all categories
    # Fetch the specific blog post by slug or return 404 if not found
    post = get_object_or_404(Blog, blog_slug=slug)
    context = {
        # 'posts': posts,
        'cat': category,
        'post': post,
    }

    return render(request, 'blog_details.html', context)


def category(request, slug):
    all_categories = Category.objects.all()  # Fetch all categories
    # Fetch the specific category by slug
    cat = get_object_or_404(Category, slug=slug)
    # Get all posts for this category
    posts = Blog.objects.filter(category=cat)
    context = {
        'category': all_categories,
        'active_category': slug,
        'posts': posts,
        'blog_cat': cat,
    }

    return render(request, 'category.html', context)
