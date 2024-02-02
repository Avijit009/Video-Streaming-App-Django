from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadVideo.as_view(), name='upload'),
    path('category/', views.VideoCategory.as_view(), name='category'),
    path('video_detail/<int:pk>/', views.VideoDetail.as_view(), name='video_detail'),
    path('<int:pk>/update', views.UpdateVideo.as_view(), name='update'),
    path('<int:pk>/remove', views.RemoveVideo.as_view(), name='remove'),
    path('list/<int:pk>', views.VideoList.as_view(), name='list'),
    path('search/', views.SearchVideo.as_view(), name='search'),
]