FROM node:10

ARG HOST_USER_ID

RUN groupmod -g ${HOST_USER_ID} node && \
    usermod -u ${HOST_USER_ID} -g ${HOST_USER_ID} node

USER node
WORKDIR /application
COPY --chown=node application /application
