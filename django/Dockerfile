FROM python:3.6

ARG HOST_USER_ID
ARG DJANGO_SECRET_KEY

RUN apt -y update && \
    apt -y install gettext && \
    \
    mkdir -p /application \
             /resources/media \
             /resources/static && \
    \
    useradd -u ${HOST_USER_ID} -ms /bin/bash user && \
    \
    chown -R user: /application \
                   /resources/media \
                   /resources/static

USER user
COPY requirements.txt /tmp
ENV PATH=/home/user/.local/bin:$PATH
RUN pip3 install --user -r /tmp/requirements.txt

COPY application /application
WORKDIR /application

RUN python manage.py collectstatic --noinput
