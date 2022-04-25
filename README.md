"# tagging_system" 

clone the repo

cd /

source env/bin/activate  # On Windows use `env\Scripts\activate`

python manage.py makemigrations
python manage.py migrate

python manage.py makemigrations core
python manage.py migrate core

python manage.py createsuperuser

python manage.py runserver

log into admin (http://127.0.0.1:8000/admin)

create user
add post

API doc: http://127.0.0.1:8000/api/docs

to see post: http://127.0.0.1:8000/api/posts

to like the post: http://127.0.0.1:8000/api/like/id  //replace id with real id number

to like the post: http://127.0.0.1:8000/api/dislike/id  //replace id with real id number

to return list of all the users who liked a post: http://127.0.0.1:8000/api/likelist/id  //replace id with real id number
