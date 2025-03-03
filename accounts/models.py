# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin  # 新增
from .utils import MyMgr


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'admin'


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    # password = models.CharField(max_length=255)
    idnumber = models.CharField(max_length=255)
    role = models.IntegerField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = "username"
    objects = MyMgr()
    is_staff = models.BooleanField(verbose_name="是否是员工", default=False)
    class_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255)
    class_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'student'


class Accuracy(models.Model):
    accuracy_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)
    accuracy_time = models.DateTimeField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accuracy'


class Answer(models.Model):
    anwer_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey('Question', models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)
    answer = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    answer_time = models.DateTimeField(blank=True, null=True)
    cnt = models.IntegerField()



    class Meta:
        managed = False
        db_table = 'answer'


class Comment(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    course_name = models.CharField(max_length=255)
    course_intro = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name
    class Meta:
        managed = False
        db_table = 'course'


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'enrollment'


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'file'


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    title = models.CharField(max_length=255)
    time = models.DateTimeField()
    content = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'post'


class PublicQuestions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=4000, blank=True, null=True)
    solution = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'public_questions'


class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    content = models.CharField(max_length=4000, blank=True, null=True)
    solution = models.CharField(max_length=255, blank=True, null=True)
    sol_reason = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    cnt = models.IntegerField(default=0)
    tag = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.content
    class Meta:
        managed = False
        db_table = 'question'


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'teacher'

class Citation(models.Model):
    citation_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', models.DO_NOTHING, blank=True, null=True)
    question = models.ForeignKey('PublicQuestions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'citation'