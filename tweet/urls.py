from django.urls import path

from .views import index, tweet_detail, tweet_list_view, tweet_create_view, anu
urlpatterns = [
    path('', index, name='home'),
    path('create-tweet', tweet_create_view, name='create_tweet'),
    path('tweets/', tweet_list_view),
    path('tweet_detail/<int:tweet_id>', tweet_detail, name='tweet'),
    path('anu/', anu, name='anu')

]
