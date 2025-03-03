from fileinput import filename
import re
from turtle import goto, left
from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect

from .models import *
from django.http import HttpResponse
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import pymysql
 
# app主页
def index_in(request):
    # print("index")
    return render(request, "createcourse/index.html")

def process_excel_file(enrollment):
    # 使用 pandas 读取 Excel 文件
    df = pd.read_excel(enrollment, engine='openpyxl')

    # 获取 student_id 列的数值
    student_ids = df['student_id'].tolist()

    # 打印每个学生的 student_id
    for student_id in student_ids:
        print(student_id)

# 加载文件上传表单
def upload(request):
    # print("upload")
    return render(request, "createcourse/upload.html")

def showresult(request):
    #判断请求类型
    if request.method == "POST":
        #获取表单数据,如果获取不到,则为None
        course_name = request.POST.get("coursename",None)
        description = request.POST.get("description", None)
        enrollment = request.FILES.get('enrollment')
        #print(enrollment)
        #process_excel_file(enrollment)
        #######################################################
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        teacher = Teacher.objects.get(user=user)
        teacher_id = teacher.teacher_id
        #######################################################
        # print(coursename, description)
        course = Course()
        course.teacher = teacher
        course.course_name = course_name
        course.course_intro = description
        course_last = Course.objects.last()
        course_id = course_last.course_id + 1
        course.course_id = course_id
        course.save()

        #res, course_id = createcourse(teacher_id, course_name, description)
        # 通过enrollment获取student_id
        # 使用 pandas 读取 Excel 文件
        print(enrollment)
        df = pd.read_excel(enrollment, engine='openpyxl')
        # 获取 student_id 列的数值
        student_ids = df['student_id'].tolist()
        # 打印每个学生的 student_id
        for studentid in student_ids:
            enroll = Enrollment()
            enroll.student = Student.objects.get(student_id=studentid)
            enroll.course = Course.objects.get(course_id=course_id)
            enroll.save()
        # 出错

    return redirect('courselist')

# 执行文件上传处理
def doupload(request):
    return redirect('/output')


def createcourse(teacher_id, course_name, description):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')

    sql = "SELECT COUNT(*) FROM course;"  
    cursor = db.cursor()
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据
    num_courses = cursor.fetchone()
    # 生成新的课程id
    new_course_id = num_courses[0] + 1

    sql = "INSERT INTO course(course_id, course_name, course_intro, teacher_id) VALUES(" + str(new_course_id) + ", \"" + course_name + "\",\"" + description + "\"," + str(teacher_id) + ");"
    # print(sql)
    try:
        cursor.execute(sql)
        # 将改动提交到数据库
        db.commit()
    except Exception as e:
        print(e)
        db.close()
        return e, new_course_id   # 创建失败，返回报错信息

    # 关闭数据库连接
    db.close()
    return None, new_course_id   # 创建成功，返回新的课程id

        

        

