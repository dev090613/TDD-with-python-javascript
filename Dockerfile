FROM python:3.11-slim

RUN addgroup --system nonroot && adduser --system --no-create-home --disabled-password --group nonroot

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

RUN python manage.py collectstatic --noinput

ENV DJANGO_DEBUG_FALSE=1
CMD gunicorn --bind :8888 superlists.wsgi:application
