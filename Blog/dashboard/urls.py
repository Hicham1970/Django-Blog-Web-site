
from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dash.html', views.dashboard, name='dashboard'),
    path('blogpost/', views.blogpost, name='blogpost'),
    path('comments/', views.comments, name='comments'),
    path('charts/', views.charts, name='charts'),
    path('pages/', views.pages, name='pages'),
]
