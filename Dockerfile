# syntax=docker/dockerfile:1
FROM python:3.11.1-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY website /website

ENV SECRET_KEY='you_django_sickret-key'

ENV DJANGO_SUPERUSER_PASSWORD=You_Admin_paword!
ENV DJANGO_SUPERUSER_EMAIL=example@example.com
ENV DJANGO_SUPERUSER_USERNAME=admin

WORKDIR /website
EXPOSE 8000

RUN pip install --no-cache-dir -r /temp/requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createcachetable

RUN python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
