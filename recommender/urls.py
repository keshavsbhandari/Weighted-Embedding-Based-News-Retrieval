from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v/',views.updateRecomList, name = 'updateRecomList'),
    path('n/',views.updateUserList, name = 'updateUserList'),
    path('d/',views.deleteUserList, name = 'deleteUserList'),
    path('u/',views.loadNewsList, name = 'updateNewsList'),
    path('r/',views.getRecommendationList, name = 'updateNewsList'),

]