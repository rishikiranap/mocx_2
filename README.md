# mocx_2

After cloning the repo, please follow the steps given below

1) Check for requirements.txt and install all the requirements
"pip install -r requirements.txt"

2) Create migrations and migrate
"python manage.py makemigrations && python manage.py migrate"
Note: Install postgresql and pgadmin4, then please check if the DATABASE-NAME(settings.py) is set to the created DB name on pgadmin

3) Runserver (localhost)
"python manage.py runserver"
