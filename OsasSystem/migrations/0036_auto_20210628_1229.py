# Generated by Django 3.0 on 2021-06-28 04:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OsasSystem', '0035_auto_20210628_1220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concept_paper_title',
            name='title_accomplish_status',
        ),
        migrations.AddField(
            model_name='concept_paper_title',
            name='title_date_accomplished',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='room_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='room_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='concept_paper_title',
            name='title_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='fund',
            name='fund_date_requested',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='officer',
            name='off_date_added',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_accreditation',
            name='acc_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_accreditation',
            name='acc_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_concept_paper',
            name='con_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='org_concept_paper',
            name='con_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization_chat',
            name='msg_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_notif',
            name='notif_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_auth_user',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_code_title',
            name='ct_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_course',
            name='course_add_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc), max_length=50),
        ),
        migrations.AlterField(
            model_name='osas_r_course',
            name='course_edit_date',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_designation_office',
            name='designation_datecreated',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_disciplinary_sanction',
            name='ds_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='osas_r_personal_info',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_personal_info',
            name='stud_birthdate',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc), max_length=12),
        ),
        migrations.AlterField(
            model_name='osas_r_section_and_year',
            name='yas_dateregistered',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_r_userrole',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_complaint',
            name='comp_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_excuse',
            name='excuse_datecreated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_excuse',
            name='excuse_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='osas_t_sanction',
            name='sanction_dateupdated',
            field=models.DateField(default=datetime.datetime(2021, 6, 28, 4, 29, 8, 887472, tzinfo=utc)),
        ),
    ]
