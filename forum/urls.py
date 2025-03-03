from django.urls import path

from . import views

urlpatterns = [
    path('index/<int:courseid>',views.index, name = 'forum_index'),
    path('post_detail/<int:postid>',views.post_detail, name = 'post_detail'),
    path('add_post', views.add_post, name='add_post'),
    path('delete_post/<int:postid>',views.delete_post, name='delete_post'),
    path('delete_comment/<int:commentid>',views.delete_comment, name='delete_comment'),
]