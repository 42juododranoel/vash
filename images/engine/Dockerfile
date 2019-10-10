FROM python:3.6-alpine

ARG USER_ID
ARG USER_NAME=user
ARG CODE_FOLDER=/code
ARG RESOURCES_FOLDER=/resources

RUN adduser -u ${USER_ID} -D ${USER_NAME} && \
    \
    mkdir -p ${CODE_FOLDER} \
             ${RESOURCES_FOLDER} && \
    \
    chown -R ${USER_NAME}: ${CODE_FOLDER} \
                           ${RESOURCES_FOLDER} && \
    \
    # g++ for Brotli
    # gcc, musl-dev, zlib-dev, jpeg-dev for Pillow
		# gifsicle to resize GIF
		# libwebp-dev to convert JPEG and PNG to Webp
		# libwebp-tools to convert GIF to Webp
    apk --no-cache add g++ \
                       gcc \
                       musl-dev \
                       zlib-dev \
                       jpeg-dev \
                       gifsicle \
                       libwebp-dev \
                       libwebp-tools

USER ${USER_NAME}
COPY requirements.txt /tmp
ENV PATH=/home/${USER_NAME}/.local/bin:${PATH}
RUN pip3 --no-cache-dir install --user -r /tmp/requirements.txt

COPY code ${CODE_FOLDER}
WORKDIR ${CODE_FOLDER}
