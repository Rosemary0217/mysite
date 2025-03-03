from django.urls import path
from . import views 
from django.conf.urls import include
from . import views

urlpatterns = [
#path("",views.index_in,name="index"),
#文件上传路由配置
path("createcourse",views.upload,name="createcourse"),
path("createcourse_upload",views.upload,name="createcourse_upload"),#加载文件上传表单页
path("createcourse_doupload",views.doupload,name="createcourse_doupload"),#执行文件上传表单
path('createcourse_result', views.showresult,name="createcourse_showresult"),           #修改录音时间
]