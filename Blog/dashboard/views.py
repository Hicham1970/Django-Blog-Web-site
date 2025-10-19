from django.shortcuts import render
from Home.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required



@login_required

def dashboard(request):
    
    total_views = Blog.objects.aggregate(total_views=Sum('views'))['total_views'] 
    total_comments = Comment.objects.count()
    total_posts = Blog.objects.count()
    post = Blog.objects.order_by('-id') # Récupère les posts les plus récents en premier
    
    context = {
        'total_views': total_views,
        'total_comments': total_comments,
        'total_posts': total_posts,
        'post': post,
    }
    
    return render(request, 'dashboard/dash.html', context )


@login_required

def blogpost(request):
    post = Blog.objects.order_by('-id') # Récupère les posts les plus récents en premier
    context = {
        'post': post,
    }
    
    return render(request, 'dashboard/blogpost.html', context )


@login_required
def comments(request):
    all_comments= Comment.objects.select_related('post').order_by('created_at') # Récupère les comments les plus récents en premier
    context = {
        'all_comments': all_comments,
    }
    
    return render(request, 'dashboard/comments.html', context )

def charts(request):
    return render(request, 'dashboard/charts.html' )


@login_required

def pages(request):
    
    return render(request, 'dashboard/pages.html' )


