from django.shortcuts import redirect, render, get_object_or_404
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
    trending = Blog.objects.filter(section='Trending').order_by(
        '-id')[:4]  # Fetch 5 trending posts   
    inspiration = Blog.objects.filter(section='Inspiration').order_by(
        '-id')[:4]  # Fetch 5 inspiration posts
    
    context = {
        'post': post,
        'main_post': main_post,
        'recent': recent,
        'popular': popular,
        'category': category,
        'trending': trending,
        'inspiration': inspiration,
        
    }

    return render(request, 'index.html', context)


def blog_details(request, slug):
    # posts = Blog.objects.order_by('-id') # Fetch all blog posts ordered by ID in descending order
    category = Category.objects.all()  # Fetch all categories
    # Fetch the specific blog post by slug or return 404 if not found
    post = get_object_or_404(Blog, blog_slug=slug)
    comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('-created_at')
    
    
    context = {
        # 'posts': posts,
        'cat': category,
        'post': post,
        'comments': comments,
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


def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug=slug)
        comment_text = request.POST.get('InputComment')
        email = request.POST.get('InputEmail')
        website = request.POST.get('InputWeb')
        name = request.POST.get('InputName')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        
        Comment.objects.create(post=post, name=name, email=email, website=website, comment_text=comment_text, parent=parent_comment)  
        
        
        return redirect('blog_details', slug=post.blog_slug)
    return redirect('blog_details')
      

       