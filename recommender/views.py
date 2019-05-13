from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import json
import random
import requests

# Create your views here.

user_path = 'data/user.json'
recom_path = 'data/recom.json'
news_path = 'data/news.json'
ids_path = 'data/ids.json'

def shuffledict(news):
    news = list(news.items())
    random.shuffle(news)
    return dict(news)

def readfile(fname):
    try:
        with open(fname, "r") as f:
            d = json.load(f)
        return d
    except:
        return None

def writefile(fname, data):
    with open(fname, 'w') as f:
        json.dump(data, f)

def index(request):
    user = readfile(user_path)
    news = readfile(news_path)
    recom = readfile(recom_path)
    if user is None:
        user = []

    if recom is None:
        recom = []

    background = {0: 'white', 1: 'lightgray'}
    readnews = []

    for i,id in enumerate(user):
        context = {}
        context['background'] = background.get(i%2)
        context['news'] = news.get(id)
        context['id'] = id
        readnews.append(context)

    allrecom = []

    for i,id in enumerate(recom):
        context = {}
        context['background'] = background.get(i % 2)
        context['news'] = news.get(id)
        context['id'] = id
        allrecom.append(context)


    allnews = [{'news':x[1],'id':x[0]} for i,x in enumerate(list(news.items())) if x[0] not in user+recom]
    for i,item in enumerate(allnews):
        item['background']=background.get(i%2)

    print(len(allnews))
    print(len(user))
    print(len(recom))
    return render(request,'recommender/index.html',{'usernews':readnews,'recomnews':allrecom,'allnews':allnews})


def getRecommendationList(request):
    background = {0: 'white', 1: 'lightgray'}
    if request.method == "POST" and request.is_ajax():
        url = "http://0.0.0.0:5002/r?n=" + request.POST.get('n')
        url_ = "http://0.0.0.0:5002/r_?n=" + request.POST.get('n')
        recomlist = requests.get(url).json()
        recomlist_ = requests.get(url_).json()
        news = readfile(news_path)
        allrecom = []
        allrecom_ = []
        for i,(recomid,recomid_) in enumerate(zip(recomlist,recomlist_)):
            context = {}
            context['id'] = recomid
            context['serial'] = i+1
            context['background'] = background.get(i%2)
            context['news'] = news.get(recomid)

            context_ = {}
            context_['id'] = recomid_
            context_['serial'] = i + 1
            context_['background'] = background.get(i % 2)
            context_['news'] = news.get(recomid_)

            allrecom.append(context)
            allrecom_.append(context_)
        data = {'custom':allrecom,'google':allrecom_}
        return HttpResponse(json.dumps(data),content_type="application/json")

def updateRecomList(request):
    # update()
    ids = readfile(ids_path)
    user = readfile(user_path)
    news = readfile(news_path)
    background = {0: 'white', 1: 'lightgray'}
    if user:
        ids = list(set(ids)-set(user))
    if request.method == "POST" and request.is_ajax():
        n = int(request.POST.get('n'))
        recom_list = random.sample(ids,n)
        writefile(recom_path,recom_list)
        allrecom = []
        for i,recomid in enumerate(recom_list):
            context={}
            context['id'] = recomid
            context['background'] = background.get(i%2)
            context['news'] = news.get(recomid)
            allrecom.append(context)
        return HttpResponse(json.dumps(allrecom),content_type="application/json")

def updateUserList(request):
    # update()
    user = readfile(user_path)
    if request.method == "POST" and request.is_ajax():
        newsid = request.POST.get('newsid')
        user.insert(0,newsid)
        writefile(user_path, user)
        return HttpResponse("Done")

def deleteUserList(request):
    # update()
    user = readfile(user_path)
    if request.method == "POST" and request.is_ajax():
        newsid = request.POST.get('newsid')
        user.remove(newsid)
        writefile(user_path,user)
        return HttpResponse("Done")


def loadNewsList(request):
    user = readfile(user_path)
    news = shuffledict(readfile(news_path))
    recom = readfile(recom_path)
    if user:
        news = {i:j for i,j in news.items() if not i in user}
    if recom:
        news = {i: j for i, j in news.items() if not i in recom}


    background = {0: 'white', 1: 'lightgray'}
    allnews = []
    for i, (id, inews) in enumerate(news.items()):
        context = {}
        context['background'] = background.get(i % 2)
        context['news'] = inews
        context['id'] = id
        allnews.append(context)

    print(len(user))
    print(len(recom))
    print(len(allnews))

    if request.method=="POST" and request.is_ajax():
        n = int(request.POST.get('n'))
        # data = {'message':{'message': "%s added" % request.POST.get('n')}}
        return HttpResponse(json.dumps(allnews[:n]), content_type="application/json")

"""
N = 20
url = "http://0.0.0.0:5002/r?n="+N
recomlist = requests.get(url).json()
"""