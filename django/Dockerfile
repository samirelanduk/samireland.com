FROM --platform=linux/amd64 python:3.8-slim-bullseye

# Create location for app
RUN mkdir -p /home/app && \
    mkdir -p /home/app/static && \
    mkdir -p /home/app/media
WORKDIR /home/app

# Install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir gunicorn psycopg2-binary -r requirements.txt && \
    rm -rf /root/.cache

# Transfer required files
COPY ./about ./about
COPY ./articles ./articles
COPY ./core ./core
COPY ./projects ./projects
COPY ./manage.py ./manage.py

# Collect static files
ARG STATIC_ROOT
ENV STATIC_ROOT $STATIC_ROOT
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", ":80", "core.wsgi:application", "--workers=16", "--log-level", "debug"]