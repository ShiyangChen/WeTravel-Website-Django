rm db.sqlite3
rm -r wetravel/migrations/

python manage.py makemigrations wetravel
python manage.py migrate
python user_population.py
python manage.py createsuperuser
