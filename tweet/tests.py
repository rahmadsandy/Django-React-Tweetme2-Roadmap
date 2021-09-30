from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Tweet

# Create your tests here.
User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cfe", password='somepassword')
        self.userb = User.objects.create_user(
            username="cfe-2", password='somepassword')
        Tweet.objects.create(content="My first Tweet", user=self.user)
        Tweet.objects.create(content="My first Tweet", user=self.user)
        Tweet.objects.create(content="My first Tweet", user=self.userb)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(
            content="My second Tweet", user=self.user)
        self.assertEquals(tweet_obj.id, 4)
        self.assertEquals(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="somepassword")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 1)
        # print(response.json())

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 3)
        # print(response.json())

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        self.assertEquals(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEquals(like_count, 1)
        # print(response.json())

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "like"})
        self.assertEquals(response.status_code, 200)
        response = client.post("/api/tweets/action/",
                               {"id": 1, "action": "unlike"})
        self.assertEquals(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEquals(like_count, 0)
        # print(response.json())

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
                               {"id": 2, "action": "retweet"})
        self.assertEquals(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2, new_tweet_id)
        self.assertEquals(self.currentCount + 1, new_tweet_id)
        # print(response.json())

    def test_tweet_create_api_view(self):
        request_data = {"content": "This is my test Tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/",
                               request_data)
        self.assertEquals(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEquals(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail_api(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEquals(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEquals(_id, 1)

    def test_tweet_delete_api(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEquals(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEquals(response.status_code, 404)
        response_incorrent_owner = client.delete("/api/tweets/3/delete/")
        self.assertEquals(response_incorrent_owner.status_code, 401)
