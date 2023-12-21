from django.urls import path, include
from . import views
 
   # Replace 'your_app' and 'custom_404_view' with actual values

from django.conf.urls import handler404
 

handler404 = 'base.views.custom_404_view'
urlpatterns = [
    
    path("videocall/", include('videocall.urls')),
    path("", views.home, name="home"),
    path("check", views.check_404, name="check"),
    path("login/", views.LoginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout!/", views.logoutUser, name="logout"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.UpdateRoom, name="update-room"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("update-user/", views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
]
