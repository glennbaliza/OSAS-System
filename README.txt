# OSASDjango
OSAS SUPPORT SYSTEM


#1 makemigrations
python manage.py makemigrations

#2 migrate
python manage.py migrate

note: if error something ODBC
run this code to mysql console.

create user ODBC identified by ''; grant all on osas.* to 'ODBC'@'%';
