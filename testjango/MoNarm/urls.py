from django.urls import path

from MoNarm.views import Hi, Arz, renderer,Becha,detailData
appName="monarm"
urlpatterns = [
    path('data/<slug:slug>',detailData, name ="detail"),
    path('',renderer , name = "renderer"),
    path('x', Arz,name="Arz"),
    path('y/', Hi,name="Hi"),
    path('users/',Becha,name="Becha")
]