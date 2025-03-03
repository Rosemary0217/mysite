from django.urls import path
from . import views 
from . import views

urlpatterns = [
path("",views.index_in,name="index"),
#文件上传路由配置
path("searchquestion",views.upload,name="searchquestion"),
path("searchquestion_upload",views.upload,name="searchquestion_upload"),#加载搜索表单页
path('searchquestion_by_tag_index', views.searchQuestionByTag_index,name="searchquestion_by_tag_index"), #学科标签选择页面
path('searchquestion_by_tag', views.searchQuestionByTag,name="searchquestion_by_tag"),  #按学科标签搜索
path('searchquestion_search', views.searchQuestion,name="searchquestion_search"),           #展示结果
path('addquestion', views.addQuestion,name="addquestion"),
]