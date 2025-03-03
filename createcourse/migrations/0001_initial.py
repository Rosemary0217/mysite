# Generated by Django 4.0.2 on 2023-10-31 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('course_intro', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'course',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PublicQuestions',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=4000, null=True)),
                ('key', models.CharField(blank=True, max_length=255, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'public_questions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('idnumber', models.CharField(max_length=255)),
                ('role', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.user')),
            ],
            options={
                'db_table': 'teacher',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.user')),
            ],
            options={
                'db_table': 'student',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=4000, null=True)),
                ('key', models.CharField(blank=True, max_length=255, null=True)),
                ('key_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.course')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.teacher')),
            ],
            options={
                'db_table': 'question',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('content', models.CharField(max_length=4000)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.user')),
            ],
            options={
                'db_table': 'post',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('filepath', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.teacher')),
            ],
            options={
                'db_table': 'file',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.student')),
            ],
            options={
                'db_table': 'enrollment',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.teacher'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('comment_time', models.DateTimeField(blank=True, null=True)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.post')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.user')),
            ],
            options={
                'db_table': 'comment',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('anwer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_time', models.DateTimeField(blank=True, null=True)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.question')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.student')),
            ],
            options={
                'db_table': 'answer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.user')),
            ],
            options={
                'db_table': 'admin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Accuracy',
            fields=[
                ('accuracy_id', models.IntegerField(primary_key=True, serialize=False)),
                ('accuracy_time', models.DateTimeField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='createcourse.question')),
            ],
            options={
                'db_table': 'accuracy',
                'managed': True,
            },
        ),
    ]
