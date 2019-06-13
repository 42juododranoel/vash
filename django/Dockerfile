FROM python:3.6-alpine

ARG HOST_USER_ID

# g++ for Brotli
# postgresql-dev for Postgres
# gcc, zlib-dev musl-dev, jpeg-dev for Filer
RUN apk --no-cache add g++ \
                       gcc \
                       zlib-dev \
                       musl-dev \
                       jpeg-dev \
                       postgresql-dev && \
    \
    adduser -u ${HOST_USER_ID} -D user && \
    \
    mkdir -p /application \
             /resources/media \
             /resources/static && \
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
