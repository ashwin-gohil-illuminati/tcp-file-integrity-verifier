from django.urls import path
from . import views

urlpatterns = [

    
    path('', views.home, name="home"),
    #path('annonymous/', views.intro, name="intro"),    
    path('login', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerPage, name = "register"),
    path('scanjobs/', views.getscanjobs, name = "scanjobs"),
    path('lastscan/', views.getlastscan, name = "lastscan"),
    path('lastrescan/', views.getlastrescan, name = "lastrescan"),
    path('getscan/', views.getscanByJob, name = "getscan"),
    path('getrescan/', views.getrescanByJob, name = "getrescan"),
    path('updateavatar', views.updateUser, name = "update-user"),
    #path('first', views.updateUser, name = "update-user"),
    path('connectinfo/', views.connectinfo, name = "connectinfo"),
    path('deletescanjob/', views.deletescanjob, name = "deletescanjob"),
    path('deleterescanjob/', views.deleterescanjob, name = "deleterescanjob"),
    path('download/', views.send_file, name='downloadfile')
]