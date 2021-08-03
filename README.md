# OSASDjango
OSAS SUPPORT SYSTEM


// if db is successfully imported.

OSAS HEAD ACCOUNT:
username: osas
password: 123

note: If osas_db.sql is not working, try to migrate the model in models.py.

//for fresh db.
-Add data to osas_r_userrole table.
user_type = HEAD OSAS && STUDENT
note: this is a hardcode value.

after creating role for OSAS HEAD, you can now proceed to adding OSAS HEAD Account (this will be his/her account to access the system for OSAS HEAD). 
go to osas_r_auth_user table then add the corresponding data.
note: Status in every table is hard coded so please use caps ex: status = 'ACTIVE'

// for creating student info (this will be used for creating organization account).
-Add courses in the osas_r_course table.
ex: 
course_name = Bachelor of science in information technology,
course_code = BSIT,
course_status = 'ACTIVE'

-Add year & section in osas_r_section_and_year table.
ex:
yas_descriptions = 4 - 1,
status = 'ACTIVE'

-Add student info in osas_r_personal_info table.
just fill it out the columns (see database schema to know what are those required and not).



