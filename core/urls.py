
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweet.urls')),
    path('mikrotik/', include('mikrotik.urls')),
]
