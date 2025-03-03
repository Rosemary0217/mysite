from django.shortcuts import render
from .models import *
import pymysql
from django.shortcuts import redirect
import re

tag_list = ["数学", "英语", "物理", "计算机"]


# app主页
def index_in(request):
    return render(request, "createcourse/index.html")


# 加载上传表单
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
        'tag_list': tag_lists,
    }
    return render(request, "searchquestion/upload.html",context)


def searchQuestionByTag_index(request):
    questions = Question.objects.all()
    tag_set = set()
    for question in questions:
        if question.tag:
            tag_set.add(question.tag)
    tag_lists = list(tag_set)
    print(tag_lists)
    return render(request, "searchquestion/search_by_tag_index.html", {"tag_list": tag_lists})


def searchQuestionByTag(request):
    #判断请求类型
    if request.method == "POST":
        #获取表单数据,如果获取不到,则为None
        tag = request.POST.get("chosen_tag", None)
        # print("tag:", tag)
        if tag is not None:
            sub_questions = searchTagInDB(tag)
        else:
            sub_questions = tuple()
        questions = PublicQuestions.objects.filter(tag=tag)
        course_id = request.session.get('courseid')
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        is_teacher = False
        if (user.role == 1):
            is_teacher = True
        course = Course.objects.get(course_id=course_id)
        context = {
            'is_teacher': is_teacher,
            'course': course,
            'course_id': course_id,
            'question_list': questions,
        }
        return render(request, "searchquestion/search_by_tag.html", context)


def searchQuestion(request):
    #判断请求类型
    if request.method == "POST":
        #获取表单数据,如果获取不到,则为None
        keyword = request.POST.get("keyword", None)
        num = request.POST.get("number", 20)
        #res = searchQuestionInDB(keyword, num)
        questions = PublicQuestions.objects.filter(content__icontains=keyword)

    course_id = request.session.get('courseid')
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    course = Course.objects.get(course_id=course_id)
    context = {
        'is_teacher': is_teacher,
        'course': course,
        'course_id': course_id,
        'questions':questions,
    }
    return render(request, "searchquestion/search_result.html", context)


def searchTagInDB(tag):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')

    sql = "SELECT * FROM question WHERE tag=\"" + tag + "\";"  
    # print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    questions = cursor.fetchall()

    db.close()
    return questions


def searchQuestionInDB(keyword, num):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')

    sql = "SELECT * FROM question;"  
    cursor = db.cursor()
    cursor.execute(sql)
    questions = cursor.fetchall()
    counter = 0

    res_set = list()
    for question in questions:
        # print(question)  # (1, '这是一道题目', '1011', None, 1, 1)
        content = question[1]
        if re.findall(keyword, content):
            # print('True')
            res_set.append(question)
            counter += 1
            if counter == num:
                break

    db.close()
    return res_set
    

def addQuestion(request):
    if request.method == "POST":
        #获取表单数据,如果获取不到,则为None
        question_id = request.POST.get("question_id", None)
        print(question_id)
        ##########################################
        course_id = request.session.get('courseid')
        ##########################################
        msg = addQuestionToDB(question_id, course_id)
    course_id = request.session.get('courseid')
    return redirect('course_detail',course_id)
 

def addQuestionToDB(question_id, course_id):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='django',
                     charset='utf8')
    cursor = db.cursor()

    # 首先检测是否已经存在在目标课程题库中
    sql_1 = "SELECT COUNT(*) FROM citation WHERE question_id=" + str(question_id) + " AND course_id=" + str(course_id) +";"
    #print(sql_1)
    cursor.execute(sql_1)
    num_existing_question = cursor.fetchone()
    if num_existing_question[0] > 0:
        return "Error：问题#" + str(question_id) + "已存在在课程#" + str(course_id) + "题库中！"
    
    sql_2 = "SELECT COUNT(*) FROM citation WHERE question_id=" + str(question_id) + " AND course_id=" + str(course_id) +";" 
    # print(sql_1) 
    cursor.execute(sql_2)
    num_existing_question = cursor.fetchone()
    if num_existing_question[0] > 0:
        return "Error：问题#" + str(question_id) + "已存在在课程#" + str(course_id) + "题库中！"

    # 题目不在目标课程的题库中，添加引用关系
    # sql = "SELECT * FROM question WHERE question_id=" + str(question_id) + ";"  
    # cursor.execute(sql)
    # question = cursor.fetchone()
    # print(question)
    
    sql = "INSERT INTO citation(question_id, course_id) VALUES("  + str(question_id) + ", " + str(course_id) + ");"
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
    return "成功添加问题#" + question_id + "到课程#" + str(course_id) +"题库！"