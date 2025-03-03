from django.urls import path
from . import views 
from django.conf.urls import include
from . import views

urlpatterns = [
#path("",views.index_in,name="index"),
#文件上传路由配置
path("createquestion",views.upload,name="createquestion"),
path("createquestion_upload",views.upload,name="createquestion_upload"),#加载文件上传表单页
path("createquestion_doupload",views.doupload,name="createquestion_doupload"),#执行文件上传表单
path('createquestion_result', views.showresult,name="createquestion_result"),           #修改录音时间
]