# from django.conf import settings
from django.urls import path
from . import views
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_details, name='blog_details'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
