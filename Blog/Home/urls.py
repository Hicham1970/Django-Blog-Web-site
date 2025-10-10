from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_details, name='blog_details'),
    path('category/<slug:slug>/', views.category, name='category'),
]
