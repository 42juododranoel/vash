FROM python:3.6

ARG HOST_USER_ID

RUN apt -y update && \
    apt -y install gettext \
                   apt-utils && \
    \
    useradd -u ${HOST_USER_ID} -ms /bin/bash user

USER user
ENV PATH=/home/user/.local/bin:$PATH

COPY requirements.txt /tmp
RUN pip3 install --user -r /tmp/requirements.txt

WORKDIR /application
