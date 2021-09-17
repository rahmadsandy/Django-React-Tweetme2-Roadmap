from django.shortcuts import render, redirect
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponse, Http404, JsonResponse
import random
from icecream import ic
from .models import Tweet
from .forms import TweetForm


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.


def index(request):
    return render(request, 'pages/home.html')


def tweet_list_view(request):
    qs = Tweet.objects.all()
    print(qs)
    tweet_list = [x.serialize() for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list,
    }
    return JsonResponse(data)


def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():

        obj = form.save(commit=False)
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


def tweet(request, tweet_id):
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
    return HttpResponse("<h1> Anu </h2>")
