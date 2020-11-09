# Generated by Django 3.0 on 2020-11-07 17:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='osas_r_course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(max_length=50, verbose_name='Course Code')),
                ('course_name', models.CharField(max_length=250, verbose_name='Course Name')),
                ('course_add_date', models.DateTimeField(blank=True, max_length=50)),
                ('course_edit_date', models.DateField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
                ('course_status', models.CharField(default='Active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='osas_r_referral',
            fields=[
                ('ref_id', models.AutoField(primary_key=True, serialize=False)),
                ('ref_name', models.CharField(max_length=250, null=True)),
                ('ref_email', models.EmailField(blank=True, max_length=50)),
                ('ref_contact', models.BigIntegerField(max_length=11, null=True)),
                ('ref_share', models.CharField(max_length=250, null=True)),
                ('ref_date_created', models.DateTimeField(max_length=50)),
                ('ref_date_updated', models.DateTimeField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
                ('status', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='osas_r_section_and_year',
            fields=[
                ('yas_id', models.AutoField(primary_key=True, serialize=False)),
                ('yas_descriptions', models.CharField(max_length=250, verbose_name='yr and sec desc')),
                ('yas_dateregistered', models.DateTimeField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
                ('status', models.CharField(default='Active', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='osas_r_stud_registration',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('s_fname', models.CharField(max_length=20)),
                ('s_lname', models.CharField(max_length=20)),
                ('s_no', models.CharField(max_length=15)),
                ('s_password', models.CharField(max_length=16)),
                ('s_type', models.CharField(default='Student', max_length=10)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='osas_r_userrole',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50, verbose_name='Full Name')),
                ('user_username', models.CharField(max_length=50, verbose_name='User Name')),
                ('user_password', models.CharField(max_length=16, verbose_name='User Password')),
                ('user_email', models.EmailField(max_length=50, verbose_name='User Email')),
                ('user_type', models.CharField(max_length=50, verbose_name='User Type')),
                ('date_created', models.DateTimeField(blank=True, max_length=50)),
                ('date_updated', models.DateTimeField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
                ('user_status', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_no', models.CharField(max_length=15, null=True)),
                ('role', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='osas_r_personal_info',
            fields=[
                ('stud_id', models.AutoField(primary_key=True, serialize=False)),
                ('stud_no', models.CharField(max_length=15, unique=True, verbose_name='Student Number')),
                ('stud_lname', models.CharField(max_length=50, verbose_name='Last Name')),
                ('stud_fname', models.CharField(max_length=50, verbose_name='First Name')),
                ('stud_mname', models.CharField(max_length=50, verbose_name='Middle Name')),
                ('stud_birthdate', models.DateField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc), max_length=12)),
                ('stud_gender', models.CharField(max_length=10, verbose_name='Gender')),
                ('stud_address', models.CharField(max_length=50, verbose_name='Student Address')),
                ('stud_email', models.EmailField(max_length=50, verbose_name='Student Email')),
                ('stud_m_number', models.BigIntegerField(blank=True, verbose_name='Mobile Number')),
                ('stud_hs', models.CharField(max_length=50, verbose_name='High School')),
                ('stud_hs_add', models.CharField(max_length=50, verbose_name='High School Address')),
                ('stud_e_name', models.CharField(max_length=50, verbose_name='Emergency Contact Person')),
                ('stud_e_address', models.CharField(max_length=50, verbose_name='Emergency Contact Address')),
                ('stud_e_m_number', models.BigIntegerField(blank=True, verbose_name='Mobile Number')),
                ('date_created', models.DateTimeField(blank=True, max_length=50)),
                ('date_updated', models.DateTimeField(default=datetime.datetime(2020, 11, 7, 17, 40, 42, 926350, tzinfo=utc))),
                ('stud_status', models.BooleanField(default=1)),
                ('stud_course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OsasSystem.osas_r_course')),
                ('stud_yas_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OsasSystem.osas_r_section_and_year')),
            ],
        ),
    ]
