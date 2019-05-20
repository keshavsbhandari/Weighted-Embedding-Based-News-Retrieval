from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import json
import random
import requests

# Create your views here.

user_path = 'data/allnews/user_all.json'
recom_path = 'data/allnews/recom_all.json'
title_path = 'data/allnews/title_all.json'
summary_path = 'data/allnews/summary_all.json'
cat_path = 'data/allnews/cat_all.json'
sitecat_path = 'data/allnews/sitecat_all.json'
ids_path = 'data/allnews/ids_all.json'
colorcat_path = 'data/allnews/colorcat.json'

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

cat = readfile(cat_path)
sitecat = readfile(sitecat_path)
summary = readfile(summary_path)
colorcat = readfile(colorcat_path)

def index(request):
    url = "http://0.0.0.0:5002/r_?n=1&s=1"
    recomid = requests.get(url).json()


    cat = readfile(cat_path)
    sitecat = readfile(sitecat_path)
    summary = readfile(summary_path)

    user = readfile(user_path)
    news = readfile(title_path)
    recom = readfile(recom_path)

    recom1 = {'news': news.get(recomid),'summary':summary.get(recomid),'cat':cat.get(recomid),'idxs':recomid,'sitecat':sitecat.get(recomid)}
    if user is None:
        user = []

    if recom is None:
        recom = []

    background = {0: 'white', 1: 'lightgray'}
    readnews = []

    for i,id in enumerate(user):
        context = {}
        context['backgrounddynamic'] = background.get(i%2)
        # context['background'] = colorcat.get(cat.get(id))
        context['news'] = news.get(id)
        context['idxs'] = id
        context['summ'] = summary.get(id)
        context['cat'] = cat.get(id)
        context['sitecat'] = sitecat.get(id)
        readnews.append(context)

    allrecom = []

    for i,id in enumerate(recom):
        context = {}
        context['backgrounddynamic'] = background.get(i % 2)
        # context['background'] = colorcat.get(cat.get(id))
        context['news'] = news.get(id)
        context['idxs'] = id
        context['summ'] = summary.get(id)
        context['cat'] = cat.get(id)
        context['sitecat'] = sitecat.get(id)
        allrecom.append(context)


    allnews = [{'news':x[1],'idxs':x[0]} for i,x in enumerate(list(news.items())) if x[0] not in user+recom]

    for i,item in enumerate(allnews):
        item['backgrounddynamic']=background.get(i%2)
        # context['background'] = colorcat.get(cat.get(item['id']))
        item['summ'] = summary.get(item['idxs'])
        item['cat'] = cat.get(item['idxs'])
        item['sitecat'] = sitecat.get(item['idxs'])


    print(len(allnews))
    print(len(user))
    print(len(recom))
    return render(request,'recommender/index.html',{'usernews':readnews,'recomnews':allrecom,'allnews':allnews,'recom':recom1})


def getRecommendationList(request):
    background = {0: 'white', 1: 'lightgray'}
    if request.method == "POST" and request.is_ajax():
        url = "http://0.0.0.0:5002/r?n=" + request.POST.get('n')
        url_ = "http://0.0.0.0:5002/r_?n=" + request.POST.get('n')
        recomlist = requests.get(url).json()
        recomlist_ = requests.get(url_).json()
        news = readfile(title_path)
        allrecom = []
        allrecom_ = []
        for i,(recomid,recomid_) in enumerate(zip(recomlist,recomlist_)):
            context = {}
            context['idxs'] = recomid
            context['serial'] = i+1
            context['backgrounddynamic'] = background.get(i%2)
            # context['background'] = colorcat.get(cat.get(recomid))
            context['news'] = news.get(recomid)
            context['summ'] = summary.get(recomid)
            context['cat'] = cat.get(recomid)
            context['sitecat'] = sitecat.get(recomid)

            context_ = {}
            context_['idxs'] = recomid_
            context_['serial'] = i + 1
            context_['backgrounddynamic'] = background.get(i % 2)
            # context['background'] = colorcat.get(cat.get(recomid_))
            context_['news'] = news.get(recomid_)

            context_['summ'] = summary.get(recomid_)
            context_['cat'] = cat.get(recomid_)
            context_['sitecat'] = sitecat.get(recomid_)


            allrecom.append(context)
            allrecom_.append(context_)
        data = {'custom':allrecom,'google':allrecom_}
        return HttpResponse(json.dumps(data),content_type="application/json")

def getRecommendationListWithSummary(request):
    background = {0: 'white', 1: 'lightgray'}
    if request.method == "POST" and request.is_ajax():
        url = "http://0.0.0.0:5002/r?n=" + request.POST.get('n')+"&s=1"
        url_ = "http://0.0.0.0:5002/r_?n=" + request.POST.get('n')+"&s=1"
        recomlist = requests.get(url).json()
        recomlist_ = requests.get(url_).json()
        news = readfile(title_path)
        allrecom = []
        allrecom_ = []
        for i, (recomid, recomid_) in enumerate(zip(recomlist, recomlist_)):
            context = {}
            context['idxs'] = recomid
            context['serial'] = i + 1
            context['backgrounddynamic'] = "#000000"
            # context['background'] = colorcat.get(cat.get(recomid))
            context['news'] = news.get(recomid)
            context['summ'] = summary.get(recomid)
            context['cat'] = cat.get(recomid)
            context['sitecat'] = sitecat.get(recomid)

            context_ = {}
            context_['idxs'] = recomid_
            context_['serial'] = i + 1
            context_['backgrounddynamic'] = background.get(i % 2)
            # context['background'] = colorcat.get(cat.get(recomid_))
            context_['news'] = news.get(recomid_)

            context_['summ'] = summary.get(recomid_)
            context_['cat'] = cat.get(recomid_)
            context_['sitecat'] = sitecat.get(recomid_)

            allrecom.append(context)
            allrecom_.append(context_)
        data = {'custom': allrecom, 'google': allrecom_}
        return HttpResponse(json.dumps(data), content_type="application/json")

def updateFeedWhenLike(request):
    ids = readfile(ids_path)
    cat = readfile(cat_path)
    sitecat = readfile(sitecat_path)
    summary = readfile(summary_path)

    user = readfile(user_path)
    news = readfile(title_path)

    recom_list = random.sample(ids, 5)
    writefile(recom_path, recom_list)

    url = "http://0.0.0.0:5002/r_?n=1&s=1"
    recomid = requests.get(url).json()

    recom_dict = {'news': news.get(recomid), 'summary': summary.get(recomid), 'cat': cat.get(recomid), 'idxs': recomid,
              'sitecat': sitecat.get(recomid)}
    if request.method == "POST" and request.is_ajax():
        newsid = request.POST.get('newsid')
        user.insert(0, newsid)
        writefile(user_path, user)
        return HttpResponse(json.dumps(recom_dict), content_type="application/json")





def updateFeedWhenDislike(request):
    ids = readfile(ids_path)
    cat = readfile(cat_path)
    sitecat = readfile(sitecat_path)
    summary = readfile(summary_path)

    user = readfile(user_path)
    news = readfile(title_path)

    recom_list = random.sample(ids, 5)
    writefile(recom_path, recom_list)
    writefile("data/allnews/custom_recom_all.json", recom_list)

    url = "http://0.0.0.0:5002/r_?n=1&s=1"
    recomid = requests.get(url).json()

    recom_dict = {'news': news.get(recomid), 'summary': summary.get(recomid), 'cat': cat.get(recomid), 'idxs': recomid,
                  'sitecat': sitecat.get(recomid)}
    if request.method == "POST" and request.is_ajax():
        return HttpResponse(json.dumps(recom_dict), content_type="application/json")

def updateRecomList(request):
    # update()
    ids = readfile(ids_path)
    user = readfile(user_path)
    news = readfile(title_path)
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
            context['idxs'] = recomid
            context['backgrounddynamic'] = background.get(i%2)
            # context['background'] = colorcat.get(cat.get(recomid))
            context['news'] = news.get(recomid)
            context['summ'] = summary.get(recomid)
            context['cat'] = cat.get(recomid)
            context['sitecat'] = sitecat.get(recomid)
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
    news = shuffledict(readfile(title_path))
    recom = readfile(recom_path)
    if user:
        news = {i:j for i,j in news.items() if not i in user}
    if recom:
        news = {i: j for i, j in news.items() if not i in recom}


    background = {0: 'white', 1: 'lightgray'}
    allnews = []
    for i, (id, inews) in enumerate(news.items()):
        context = {}
        context['backgrounddynamic'] = background.get(i % 2)
        # context['background'] = colorcat.get(cat.get(id))
        context['news'] = inews
        context['idxs'] = id
        context['summ'] = summary.get(id)
        context['cat'] = cat.get(id)
        context['sitecat'] = sitecat.get(id)
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