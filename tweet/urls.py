from django.urls import path

from .views import index, tweet, tweet_list_view, tweet_create_view
urlpatterns = [
    path('', index, name='home'),
    path('create-tweet/', tweet_create_view, name='create_tweet'),
    path('tweets/', tweet_list_view),
    path('tweets/<int:tweet_id>', tweet, name='tweet'),

]
