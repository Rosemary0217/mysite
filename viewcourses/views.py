from fileinput import filename
from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect
import numpy as np
#import pylab as plt
from django.shortcuts import render
import time
import pymysql 


def index_in(request):
    return render(request, "createcourse/index.html")

def upload(request):
    #######################################################
    teacher_id = 1
    #######################################################
    course_list = searchCourses(teacher_id)
    print(course_list)
    # 出错
    if not course_list:
        return render(request, "viewcourses/upload.html", {"msg": "暂无课程"})
    # 创建成功
    else:
        return render(request, "viewcourses/upload.html", {"course_list": course_list})
    

def showresult(request): 
    #判断请求类型
    if request.method == "POST":
        #获取表单数据,如果获取不到,则为None
        course_id = request.POST.get("course_info",None)
        print("课程id:", course_id)
        course_info = getCourseInfo(course_id)
        print("课程信息:", course_info)
    return render(request, "viewcourses/result.html", {"course_info": course_info})

# 执行文件上传处理
def doupload(request):
    global recordflag
    print("output")
    return redirect('/output')

def searchCourses(teacher_id):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')

    sql = "SELECT * FROM course WHERE teacher_id = " + str(teacher_id) + ";"  
    cursor = db.cursor()
    cursor.execute(sql)
    courses = cursor.fetchall()

    return courses

def getCourseInfo(course_id):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')
    
    sql = "SELECT * FROM course WHERE course_id = " + str(course_id) + ";"  
    cursor = db.cursor()
    cursor.execute(sql)
    course_info = cursor.fetchone()

    return course_info

        

        

