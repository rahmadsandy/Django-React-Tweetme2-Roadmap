from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponse, Http404, JsonResponse
import random
from icecream import ic
from .models import Tweet, TweetLike
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer


from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.


def home_view(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'pages/home.html', context={"username": username}, status=200)


def ori(request):
    return render(request, 'pages/ori.html')


@api_view(['GET'])
def tweet_list_view(request):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


def tweet_list_view_pure_django(request):
    qs = Tweet.objects.all()
    print(qs)
    tweet_list = [x.serialize() for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list,
    }
    return JsonResponse(data)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request):
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


def tweet_create_view_pure_django(request):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():

        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', context={"form": form})


@api_view(['GET'])
def tweet_detail_view(request, tweet_id):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You Cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet Removed"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request):
    print(request.data, request.POST)
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=obj,
                content=content,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
    return Response({}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view_test(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            # this is todo
            pass
    return Response({"message": "Tweet removed"}, status=200)


def tweet_detail_pure_django(request, tweet_id):
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not Found"
        status = 404

    return JsonResponse(data, status=status)


def anu(request):
    qs = TweetLike.objects.all()
    ic(qs)
    return HttpResponse(qs)
