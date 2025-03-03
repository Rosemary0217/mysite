from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.http import HttpResponse
from .models import *
from django.utils.safestring import mark_safe

def index(request, courseid):
    # 当前访问页码 默认page = 1
    page = int(request.GET.get('page',1))
    page_size = 30
    start = (page - 1) * page_size
    end = page * page_size
    posts = Post.objects.filter(course_id=courseid).select_related('user')[start:end]

    # 计算一共需要多少页
    total_posts = Post.objects.filter(course_id=courseid).select_related('user')
    total_count = total_posts.count()
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1
    if total_page_count == 0:
        total_page_count += 1
    # 一共显示10页
    plus = 5
    # 数据库中页数比较少
    if total_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count
    # 数据库中页数比较多
    else:
        # 当前页数小于5
        if page <= plus:
            start_page = 1
            end_page = 2 * plus
        else:
            # 当前页数+5大于总页数
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 生成对应html页码
    page_str_list =[]
    # 首页
    first_page = '<li><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(first_page)
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">《</a></li>'.format(page-1)
    else:
        prev = '<li><a href="?page={}">《</a></li>'.format(1)
    page_str_list.append(prev)

    # 页码
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        next_page = '<li><a href="?page={}">》</a></li>'.format(page+1)
    else:
        next_page = '<li><a href="?page={}">》</a></li>'.format(total_page_count)
    page_str_list.append(next_page)

    # 尾页
    last_page = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(last_page)

    page_string = mark_safe("".join(page_str_list))

    # 使用session会话记住courseid
    request.session['courseid'] = courseid
    course = Course.objects.get(course_id=courseid)
    # 获取个人信息
    userid = request.session.get('userid')
    user = User.objects.get(user_id=userid)
    is_teacher = False
    if (user.role == 1):
        is_teacher = True
    return render(request, 'index.html',{'posts': posts, 'course_id': courseid, 'page_string':page_string, 'course':course, 'is_teacher':is_teacher})

def post_detail(request, postid):
    # 在帖子详情界面添加评论
    if request.method == 'POST':
        comment = Comment()
        comment.post = Post.objects.get(post_id=postid)
        # 需要从session会话中获得当前用户id
        userid = request.session.get('userid')
        comment.user = User.objects.get(user_id=userid)
        comment.comment_time = datetime.now()
        comment.content = request.POST['comment']
        comment.save()
    # 从数据库中查询帖子的详细内容
    post = Post.objects.get(post_id=postid)
    # 使用session会话记住postid
    request.session['postid'] = postid
    # 查询帖子发起人信息
    user = User.objects.get(user_id=post.user_id)
    # 从session 会话中获得当前用户id 现在设为1
    cur_user = User.objects.get(user_id=request.session.get('userid'))
    #cur_user = User.objects.get(user_id=1)
    # 查询帖子的相关评论，关联查询评论人相关信息
    comments = Comment.objects.filter(post_id=post.post_id).select_related('user')

    courseid = request.session.get('courseid')
    course = Course.objects.get(course_id=courseid)
    # 获取个人信息
    #userid = request.session.get('userid')
    #user = User.objects.get(user_id=userid)
    is_teacher = False
    if (cur_user.role == 1):
        is_teacher = True
    context = {'course': course,
               'course_id': courseid,
               'is_teacher': is_teacher,
               'post':post,
               'user':user,
               'comments':comments,
               'cur_user':cur_user,}
    return render(request,'post_detail.html',context)

def add_post(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.time = datetime.now()
        courseid = request.session.get('courseid')
        post.course = Course.objects.get(course_id=courseid)
        ##  在用户登录时通过session记住登陆的userid
        userid = request.session.get('userid')
        post.user = User.objects.get(user_id=userid)
        post.save()

        #  发布帖子成功之后，返回到论坛主页
        posts = Post.objects.filter(course_id=courseid).select_related('user')
        course = Course.objects.get(course_id=courseid)
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        is_teacher = False
        if (user.role == 1):
            is_teacher = True
        return render(request, 'index.html', {'posts': posts, 'course_id': courseid, 'course':course, 'is_teacher':is_teacher})
    else:

        # 使用session会话记住courseid
        courseid = request.session.get('courseid')
        course = Course.objects.get(course_id=courseid)
        # 获取个人信息
        userid = request.session.get('userid')
        user = User.objects.get(user_id=userid)
        is_teacher = False
        if (user.role == 1):
            is_teacher = True
        context = {'course':course,
                   'course_id':courseid,
                   'is_teacher':is_teacher}
        return render(request,'add_post.html',context)


def delete_post(request,postid):
    post = Post.objects.get(post_id=postid)
    post.delete()
    # 删除帖子成功之后，返回论坛主页
    courseid = request.session.get('courseid')
    return index(request,courseid)

def delete_comment(request,commentid):
    comment = Comment.objects.get(comment_id=commentid)
    postid = comment.post_id
    comment.delete()
    # 删除评论成功之后，返回该帖子详情
    return post_detail(request,postid)