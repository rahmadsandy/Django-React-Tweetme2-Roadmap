from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
import random
from icecream import ic
from .models import Tweet
from .forms import TweetForm

# Create your views here.


def index(request):
    return render(request, 'pages/home.html')


def tweet_list_view(request):
    qs = Tweet.objects.all()
    tweet_list = [{
        "id": x.id,
        "content": x.content,
        "likes": random.randint(0, 122),
        "dislikes": random.randint(0, 20),
    } for x in qs]

    data = {
        "isUser": False,
        "response": tweet_list,
    }
    return JsonResponse(data)


def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    ic(next_url)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if next_url != None:
                return redirect(next_url)
            form = TweetForm()

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
