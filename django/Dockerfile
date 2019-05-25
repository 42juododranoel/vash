FROM python:3.6-alpine

ARG HOST_USER_ID

RUN apk add gcc \
            zlib-dev \
            musl-dev \
            jpeg-dev \
            postgresql-dev && \
    \
    rm -rf /var/cache/apk/* && \
    \
    mkdir -p /application \
             /resources/media \
             /resources/static && \
    \
    adduser -u ${HOST_USER_ID} -D user && \
    \
    chown -R user: /application \
                   /resources/media \
                   /resources/static

USER user
COPY requirements.txt /tmp
ENV PATH=/home/user/.local/bin:$PATH
RUN pip3 --no-cache-dir install --user -r /tmp/requirements.txt

COPY application /application
WORKDIR /application
