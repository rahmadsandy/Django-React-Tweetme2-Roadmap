from django.urls import path

from .views import (
    index,
    tweet_detail,
    tweet_list_view,
    tweet_create_view,
    tweet_delete, anu,
    tweet_action_view,
    tweet_action_view_test,
    ori,


)

urlpatterns = [
    path('', index, name='home'),
    path('create-tweet', tweet_create_view, name='create_tweet'),
    path('tweets/', tweet_list_view),
    path('tweet_detail/<int:tweet_id>', tweet_detail, name='tweet'),
    path('api/tweets/<int:tweet_id>/delete',
         tweet_delete, name='tweet-delete'),
    path('api/tweets/action',
         tweet_action_view, name='tweet-action'),
    path('test/api/tweets/action',
         tweet_action_view_test, name='tweet-action-test'),
    path('ori', ori, name='ori'),
    path('anu/', anu, name='anu'),

]
