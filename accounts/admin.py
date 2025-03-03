from django import forms
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin, ImportMixin
from import_export import resources, fields
from import_export.forms import ImportForm, ConfirmImportForm, ExportForm
from import_export.widgets import ForeignKeyWidget

from .models import *


# from .models import User


class userresource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ('user_id',)
        fields = ['user_id', 'password', 'username', 'idnumber', 'role', 'name']
        export_order = ['user_id', ]


class teacherresource(resources.ModelResource):
    user = fields.Field(
        column_name='username',
        attribute='user',
        widget=ForeignKeyWidget(User, field='username'))

    class Meta:
        model = Teacher
        import_id_fields = ('teacher_id',)
        fields = ['teacher_id', 'user', 'name']


class studentresource(resources.ModelResource):
    user = fields.Field(
        column_name='username',
        attribute='user',
        widget=ForeignKeyWidget(User, field='username'))

    class Meta:
        model = Student
        import_id_fields = ('student_id',)
        fields = ['student_id', 'user', 'name','class_id']
        export_order = ['student_id', 'class_id']


class useradmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    resource_classes = [userresource]
    list_display = ('user_id', 'name', 'username', 'role')
    list_filter = ('username', 'role')


class teacheradmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin, ):
    resource_classes = [teacherresource]
    list_display = ('teacher_id', 'name', 'user')
    list_filter = ('name',)


class studentadmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin, ):
    resource_classes = [studentresource]
    list_display = ('student_id', 'name', 'user','class_id')
    list_filter = ('name','class_id')


admin.site.register(User, useradmin)
admin.site.register(Student, studentadmin)
admin.site.register(Teacher, teacheradmin)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Question)
admin.site.register(Answer)
