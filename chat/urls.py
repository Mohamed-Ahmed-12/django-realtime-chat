from django.urls import path
from . import views
urlpatterns = [
    path('video/<str:room_name>/',views.video_call , name='video'),
    path('chat/<str:room_name>/',views.room , name='room'),
    
]
