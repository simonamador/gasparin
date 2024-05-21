from django.urls import path

from . import views

app_name = 'video_processing'
urlpatterns = [
    path("", views.index, name="index"),
    path("video_feed", views.video_feed, name="video_feed"),
    path("live_video_feed", views.live_video_feed, name="live_video_feed"),
    path("legend_feed", views.legend_feed, name="legend_feed"),
]
