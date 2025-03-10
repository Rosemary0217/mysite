# Generated by Django 4.2.6 on 2023-11-03 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accuracy',
            fields=[
                ('accuracy_id', models.IntegerField(primary_key=True, serialize=False)),
                ('accuracy_time', models.DateTimeField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'accuracy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('anwer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('answer_time', models.DateTimeField(blank=True, null=True)),
                ('cnt', models.IntegerField()),
            ],
            options={
                'db_table': 'answer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
                ('comment_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=255)),
                ('course_intro', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'enrollment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('filepath', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'file',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('content', models.CharField(max_length=4000)),
            ],
            options={
                'db_table': 'post',
                'managed': False,
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
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.IntegerField(primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, max_length=4000, null=True)),
                ('solution', models.CharField(blank=True, max_length=255, null=True)),
                ('sol_reason', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('cnt', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'question',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'teacher',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('idnumber', models.CharField(max_length=255)),
                ('role', models.IntegerField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='是否是员工')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
        ),
    ]
