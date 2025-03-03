from django.urls import path
from . import views 
from django.conf.urls import include
from viewcourses import views 

urlpatterns = [
path("viewcoursesindex",views.index_in,name="index"),
#文件上传路由配置
path("viewcourses",views.upload,name="viewcourses"),
path("viewcourses_upload",views.upload,name="viewcourses_upload"),#加载文件上传表单页
path("viewcourses_doupload",views.doupload,name="viewcourses_doupload"),#执行文件上传表单
path('viewcourses_result', views.showresult,name="viewcourses_showresult"),           #修改录音时间
]