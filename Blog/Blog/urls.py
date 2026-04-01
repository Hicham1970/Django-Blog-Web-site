
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('dashboard/', include('dashboard.urls')),


]

# Static/media serving handled by vercel.json
