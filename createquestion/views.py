from fileinput import filename
from turtle import goto, left
from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
#import requests
import numpy as np
#import pylab as plt
from django.shortcuts import render
import pymysql
from .models import *

# question_num = 0
class Question_self():
    def __init__(self, content, answer, tag, teacher_id, course_id, public_flag):
        self.content = content
        self.answer = answer
        self.tag = tag
        self.teacher_id = teacher_id
        self.course_id = course_id
        self.public_flag = public_flag
        self.key_reason = ""
        self.question_id = -1


# app主页
def index_in(request):
    return render(request, "createcourse/index.html")

# 加载文件上传表单
def upload(request):
    course_id = request.session.get('courseid')
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    course = Course.objects.get(course_id=course_id)

    questions = Question.objects.all()
    tag_set = set()
    for question in questions:
        if question.tag:
            tag_set.add(question.tag)
    tag_lists = list(tag_set)
    print(tag_lists)
    context = {
        'is_teacher': is_teacher,
        'course': course,
        'course_id': course_id,
        'tag_list':tag_lists,
    }
    return render(request, "createquestion/upload.html",context)

# 执行数据库操作并返回结果
def showresult(request):
    # 判断请求类型
    if request.method == "POST":
        # 获取表单数据,如果获取不到,则为None
        content = request.POST.get("content", None)
        answer = request.POST.getlist("option", [])
        public_flag = True if request.POST.get("choice", None) == '1' else False
        tag = request.POST.get("tag", None)

        # 对answer进行编码
        answer_str = ""
        for op in ['A', 'B', 'C', 'D']:
            if op in answer:
                answer_str += op
        #######################################################
        userid = request.session.get('userid')
        course_id = request.session.get('courseid')
        teacher = Teacher.objects.get(user__user_id=userid)
        teacher_id = teacher.teacher_id
        #course_id = 1
        #######################################################
        question = Question()
        question.content = content
        question.solution = answer_str
        question.tag = tag
        question.course = Course.objects.get(course_id=course_id)
        question.teacher = teacher
        question_last = Question.objects.last()
        question_id = question_last.question_id + 1
        question.question_id = question_id
        question.save()

        if (public_flag):
            publicquestion = PublicQuestions()
            publicquestion.question_id = question_id
            publicquestion.content = content
            publicquestion.solution = answer_str
            publicquestion.tag = tag
            publicquestion.save()
        #question = Question_self(content, answer_str, tag, teacher_id, course_id, public_flag)
        #res = createquestion(question)
        # print(type(res))
        # 出错
        #if res:
            #msg = "创建失败！错误信息：" + res
        # 创建成功
        #else:
        #    msg = "创建成功！"

    return redirect('course_detail',course_id)
    #return render(request, "createquestion/result.html", {'course_id':course_id})


# 执行文件上传处理
def doupload(request):
    # print("output")
    return redirect('/output')

def createquestion(question):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')

    sql = "SELECT COUNT(*) FROM question;"  
    cursor = db.cursor()
    cursor.execute(sql)
    question_num = cursor.fetchone()
    # 生成新的课程id
    new_question_id = question_num[0] + 1 + 1

    sql = "INSERT INTO question(question_id, content, solution, course_id, teacher_id, tag) VALUES(" + str(
        new_question_id) + ", \"" + question.content + "\", \"" + question.answer + "\", " + str(
        question.course_id) + ", " + str(question.teacher_id) + ", \"" + question.tag + "\");"
    print(sql)
    try:
        cursor.execute(sql)
        # 将改动提交到数据库
        db.commit()
    except Exception as e:
        print(e)
        db.close()
        return e

    if question.public_flag:
        sql = "INSERT INTO public_questions(question_id, content, solution, tag) VALUES("  + str(
            new_question_id) + ", \"" + question.content + "\", \"" + question.answer + "\", \"" + question.tag + "\");"
        # print(sql)
        try:
            cursor.execute(sql)
            # 将改动提交到数据库
            db.commit()
        except Exception as e:
            print(e)
            db.close()
            return e
    # 关闭数据库连接
    db.close()
    return None




        

        

