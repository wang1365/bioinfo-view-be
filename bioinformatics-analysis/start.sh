#!/bin/zsh

#python manage.py collectstatic --noinput&&
#python manage.py makemigrations&&
#python manage.py migrate --settings=bioinformatics.settings.prod&&
python manage.py init_user --settings=bioinformatics.settings.prod&&
python manage.py init_config --settings=bioinformatics.settings.prod&&
uwsgi --env DJANGO_SETTINGS_MODULE=bioinformatics.settings.prod --ini /bioinformatics-analysis/uwsgi.ini