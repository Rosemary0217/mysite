from django.urls import path
from . import views 
from django.conf.urls import include
from uploadfile import views 

urlpatterns = [
#path("",views.index_in,name="index"),
#文件上传路由配置
path("uploadfile",views.upload,name="uploadfile"),
path("uploadfile_upload",views.upload,name="uploadfile_upload"),#加载文件上传表单页
path("uploadfile_doupload",views.doupload,name="uploadfile_doupload"),#执行文件上传表单
path('uploadfile_result', views.showresult,name="uploadfile_showresult"),           #修改录音时间
]