from django.urls import path

from .views import index, tweet, tweet_list_view
urlpatterns = [
    path('', index, name='home'),
    path('tweets/', tweet_list_view),
    path('tweets/<int:tweet_id>', tweet, name='tweet')
]
