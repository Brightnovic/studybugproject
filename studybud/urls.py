
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.shortcuts import render
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.views.static import serve 

handler404 = 'base.views.custom_404_view'
 
urlpatterns = [
 
    path('admin/', admin.site.urls),
    
    path('', include('base.urls')),
    path('videocall/', include('videocall.urls')),
    path('chat/', include('privatechat.urls')),
    path('api/', include('base.api.urls')),
 
   
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)