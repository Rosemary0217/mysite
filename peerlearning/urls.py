from django.urls import path

from . import views

urlpatterns = [
    path('index_teacher',views.indexteacher, name = 'indexteacher'),
    path('courselist',views.courselist, name = 'courselist'),
    path('course_detail/<int:courseid>',views.course_detail, name = 'course_detail'),
    path('question_list/<int:courseid>',views.question_list, name = 'question_list'),
    path('question_detail/<int:questionid>',views.question_detail, name = 'question_detail'),
    path('publish_question/<int:questionid>',views.publish_question, name = 'publish_question'),
    path('stop_question/<int:questionid>', views.stop_question, name='stop_question'),
    path('question_statu/<int:questionid>', views.question_statu, name='question_statu'),
    path('index_student',views.index_student,name = 'index_student'),
    path('answer_question/<int:courseid>',views.answer_question,name = 'answer_question'),
    path('download_file<int:fileid>',views.download_file, name = 'download_file'),
    path('review_history',views.review_history,name= 'review_history'),
    path('delete_question/<int:questionid>',views.delete_question, name = 'delete_question'),
    path('delete_file/<int:fileid>',views.delete_file,name = 'delete_file'),
    path('edit_question/<int:questionid>',views.edit_question,name = 'edit_question'),
    path('accuracy_dis/<int:questionid>',views.accuracy_rate, name = 'accuracy_dis'),
    path('delete_course/<int:courseid>',views.delete_course, name = 'delete_course')
]