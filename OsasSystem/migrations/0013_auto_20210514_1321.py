# Generated by Django 3.0 on 2021-05-14 05:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OsasSystem', '0012_auto_20210514_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='room_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='room_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='concept_paper_title',
            name='title_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='concept_paper_title',
            name='title_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='org_accreditation',
            name='acc_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_accreditation',
            name='acc_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_concept_paper',
            name='con_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_concept_paper',
            name='con_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization_chat',
            name='msg_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_notif',
            name='notif_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_auth_user',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_code_title',
            name='ct_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_course',
            name='course_add_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc), max_length=50),
        ),
        migrations.AlterField(
            model_name='osas_r_course',
            name='course_edit_date',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_designation_office',
            name='designation_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_disciplinary_sanction',
            name='ds_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='osas_r_personal_info',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_personal_info',
            name='stud_birthdate',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc), max_length=12),
        ),
        migrations.AlterField(
            model_name='osas_r_section_and_year',
            name='yas_dateregistered',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_userrole',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_complaint',
            name='comp_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_excuse',
            name='excuse_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_excuse',
            name='excuse_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_sanction',
            name='sanction_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 5, 14, 5, 21, 47, 62063, tzinfo=utc)),
        ),
    ]
