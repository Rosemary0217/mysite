import os.path
import itertools
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from itertools import chain
from .models import *
from forum.models import *
from django.conf import settings
import uuid
import matplotlib.pyplot as plt
from io import BytesIO  # 引入BytesIO类
import base64
# Create your views here.
def indexteacher(request):
    # 老师主页面，暂时绑定userid = 1
    # userid = 1
    # request.session['userid'] = userid
    return render(request,'indexteacher.html')

# 获取课程列表
def courselist(request):
    # 登录之后通过会话记住用户id
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)

    # 如果 role = 1 说明是老师
    if (user.role == 1):
        teacher = Teacher.objects.get(user__user_id=userid)
        courses = Course.objects.filter(teacher__teacher_id=teacher.teacher_id)
    # 如果role = 2  说明是学生
    if (user.role == 2):
        student = Student.objects.get(user__user_id=userid)
        courses = Course.objects.filter(enrollment__student=student)

    #userid = request.session.get('userid')
    #user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    return render(request,'courselist.html',{'courses':courses,'is_teacher':is_teacher,})

# 获得课程详情
def course_detail(request,courseid):

    # 上传文件
    if request.method == 'POST':
        file = request.FILES.get('file')
        # print(file, type(file))
        # Deeplearning深度学习笔记v5.6.pdf <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
        # file_name = file.name 不适用原文件名称存入后台
        file_name = str(uuid.uuid4()) + file.name[file.name.rfind('.'):]
        # 1. 将文件上传到后台对应的文件中
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        # print('file_path:',file_path)
        # file_path: C:\Users\29503\PycharmProjects\pythonProject\mysite\static\files\Deeplearning深度学习笔记v5.6.pdf
        with open(file_path, 'ab') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
                fp.flush()

        # 2. 将后台文件路径写入对应数据库中
        db_file = File()
        db_file.filename = file.name
        db_file.filepath = file_path
        course = Course.objects.get(course_id=courseid)
        db_file.course = course
        db_file.teacher = course.teacher
        db_file.save()

    course = Course.objects.get(course_id=courseid)
    # 通过session 将courseid存起来
    request.session['courseid']=courseid
    # 获得课程相关的文件
    files = File.objects.filter(course__course_id=courseid)
    # 获得当前用户id，只有当前用户角色为老师，课程详情页面才会显示隶属题目
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    flag = False
    is_teacher = False

    # 问题列表
    questions = Question.objects.filter(course__course_id=courseid)
    citations = Citation.objects.filter(course__course_id=courseid)
    question_cite = []
    for citation in citations:
        question_cite.append(citation.question)
    questions = chain(questions,question_cite)
    question_num = 3
    selected_questions = list(itertools.islice(questions, question_num))

    if (user.role == 1):
        flag = True
        is_teacher = True
    context = {
        'course': course,
        'files': files,
        'flag': flag,
        'is_teacher':is_teacher,
        'questions': selected_questions,
    }
    return render(request, 'course_detail.html', context)


# 获得题目列表
def question_list(request, courseid):
    questions = Question.objects.filter(course__course_id=courseid)
    citations = Citation.objects.filter(course__course_id=courseid)
    question_cite = []
    for citation in citations:
        question_cite.append(citation.question)
    questions = chain(questions,question_cite)


    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    courseid = request.session.get('courseid')
    course = Course.objects.get(course_id = courseid)
    context = {
        'is_teacher':is_teacher,
        'questions':questions,
        'course':course,
        'course_id':courseid,
    }
    return render(request,'question_list.html',context)


# 获得题目详情
def question_detail(request, questionid):
    question = Question.objects.get(question_id=questionid)
    course_id = request.session.get('courseid')
    # 刚进入时设置正确率为100%
    accuracy = 1.0

    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    #courseid = request.session.get('courseid')
    course = Course.objects.get(course_id = course_id)
    context = {
        'is_teacher':is_teacher,
        'question':question,
        'accuracy':accuracy,
        'course':course,
        'course_id':course_id,
    }
    # context = {
    #     'question':question,
    #     'accuracy':accuracy,
    #     'course_id':course_id,
    # }
    return render(request,'question_detail.html',context)

# 老师发布题目后，将对应题目is_active设为true
def publish_question(request, questionid):
    question = Question.objects.get(question_id=questionid)
    question.is_active = True
    question.save()
    return question_detail(request,questionid)

# 老师停止答题后，将对应题目is_active设为false，并获取对应正确率
def stop_question(request,questionid):
    question = Question.objects.get(question_id=questionid)
    question.is_active = False
    question.cnt = question.cnt + 1
    question.save()
    return question_detail(request,questionid)

# 老师查看正确率
def question_statu(request,questionid):
    question = Question.objects.get(question_id=questionid)
    answers = Answer.objects.filter(question=question)
    answers = answers.filter(cnt=question.cnt)
    total_answers = answers.count()
    correct_answers = answers.filter(answer=question.solution).count()
    accuracy_rate = (correct_answers / total_answers) * 100 if total_answers > 0 else 0

    # 查看完正确率之后，将正确率写入到对应的accuracy中
    accuracy = Accuracy()
    accuracy.question = question
    accuracy.rate = accuracy_rate
    accuracy.accuracy_time = datetime.now()
    userid = request.session.get('userid')
    accuracy.teacher = Teacher.objects.get(user__user_id=userid)
    accuracy.save()

    course_id = request.session.get('courseid')
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    #courseid = request.session.get('courseid')
    course = Course.objects.get(course_id = course_id)
    context = {
        'is_teacher':is_teacher,
        'question':question,
        'accuracy':accuracy_rate,
        'course':course,
        'course_id':course_id,
    }

    return render(request,'question_detail.html',context)


def index_student(request):
    # 学生主页面，暂时绑定 userid = 2
    # userid = 2
    # request.session['userid'] = userid
    return render(request,'index_student.html')


# 学生点击答题后，获取当前课程对应题目is_active = True的题目
# question_student,表示呈现给学生的问题界面
def answer_question(request,courseid):

    questions = Question.objects.filter(course__course_id=courseid)
    active_question = questions.filter(is_active=True).first()
    is_answered = False
    if request.method == 'POST':
        answer = Answer()
        answer.question = active_question
        answer.cnt = active_question.cnt + 1
        # 学生id
        userid = request.session.get('userid')
        answer.student = Student.objects.get(user__user_id=userid)

        #answer.answer = request.POST['answer']
        tmp_answer = request.POST.getlist("option", [])
        answer_str = ""
        for op in ['A', 'B', 'C', 'D']:
            if op in tmp_answer:
                answer_str += op
            #else:
            #    answer_str += "0"
        answer.answer = answer_str

        answer.reason = request.POST['reason']
        answer.answer_time = datetime.now()
        answer.save()
        # 学生回答问题之后，显示正确答案以及正确答案原因
        is_answered = True
        course_id = courseid
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        is_teacher = False
        if (user.role == 1):
            is_teacher = True
        # courseid = request.session.get('courseid')
        course = Course.objects.get(course_id=course_id)
        context = {
            'is_teacher': is_teacher,
            'question': active_question,
            'is_answered': is_answered,
            'course': course,
            'course_id': courseid,
            'answer': answer,
        }
        return render(request, 'answer_question.html', context)
    course_id = courseid
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    # courseid = request.session.get('courseid')
    course = Course.objects.get(course_id=course_id)
    context = {
        'is_teacher': is_teacher,
        'question': active_question,
        'is_answered':is_answered,
        'course': course,
        'course_id': courseid,
    }
    return render(request,'answer_question.html',context)

# 下载文件
def download_file(request,fileid):
    file = File.objects.get(file_id=fileid)
    file_path = file.filepath
    file_name = file.filename
    with open(file_path, 'rb') as fp:
        response = HttpResponse(fp.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        return response

# 学生回顾历史
def review_history(request):
    course_filter = request.GET.get('course', '')
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    answers = Answer.objects.filter(student__user=user).select_related('question','question__course')
    student = Student.objects.get(user=user)
    courses = Course.objects.filter(enrollment__student=student)


    return render(request,'history.html',{'answers':answers,'courses':courses,'course_filter':course_filter})

def delete_question(request,questionid):
    question = Question.objects.get(question_id = questionid)
    course_id = question.course.course_id
    question.delete()
    return redirect('question_list',course_id)


def delete_file(request,fileid):
    file = File.objects.get(file_id=fileid)
    course_id = file.course.course_id
    file.delete()
    return redirect('course_detail',course_id)

def edit_question(request,questionid):
    if request.method == 'GET':
        question = Question.objects.get(question_id=questionid)
        print(question.question_id, question.content, question.solution)

        course_id = request.session.get('courseid')
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        is_teacher = False
        if (user.role == 1):
            is_teacher = True
        # courseid = request.session.get('courseid')
        course = Course.objects.get(course_id=course_id)
        context = {
            'is_teacher': is_teacher,
            'course': course,
            'course_id': course_id,
            'question':question,
            'solution':question.solution,
        }
        return render(request, 'edit_question.html', context)

    if request.method == 'POST':
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
            #else:
            #    answer_str += "0"
        print(content, answer_str, public_flag, tag)
        question = Question.objects.get(question_id=questionid)
        question.content = content
        question.solution = answer_str
        question.tag = tag
        question.save()

        if public_flag:
            public_question = PublicQuestions()
            public_question.content = content
            public_question.solution = answer_str
            public_question.tag = tag
            public_question.save()


        #######################################################
        return redirect('question_detail',questionid)



def accuracy_rate(request,questionid):
    accuracies = Accuracy.objects.filter(question__question_id = questionid)
    rates = [accuracy.rate for accuracy in accuracies]
    x = range(1, len(rates) + 1)
    plt.figure(figsize=(13,6))
    bars = plt.bar(x,rates)
    plt.xlabel('Index')
    plt.ylabel('Accuracy Rate')
    plt.title('Accuracy Rate Over time')
    plt.xticks(x)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, round(yval, 2), ha='center', va='bottom', fontsize=6)
    # 保存图表到内存q
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 将图表转换为base64编码的字符串
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # 清空图表以便下次使用
    plt.clf()

    return render(request,'accuracy.html',{'accuracy_image':image_base64})

def delete_course(request,courseid):
    course = Course.objects.get(course_id=courseid)
    course.delete()
    return redirect('courselist')