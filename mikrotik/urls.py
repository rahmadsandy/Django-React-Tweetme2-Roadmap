from django.urls import path

from .views import hotspot_active
urlpatterns = [
    path('', hotspot_active, name='hotspot-active')
]
