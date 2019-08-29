FROM node:10

ARG USER_ID
ARG CODE_FOLDER=/code
ARG ASSETS_FOLDER=/resources/assets
ARG STYLES_FOLDER=/resources/styles
ARG SCRIPTS_FOLDER=/resources/scripts
ARG RESOURCES_FOLDER=/resources

RUN groupmod -g ${USER_ID} node && \
    usermod -u ${USER_ID} -g ${USER_ID} node && \
    \
    mkdir -p ${CODE_FOLDER} \
             ${RESOURCES_FOLDER} \
             ${ASSETS_FOLDER} \
             ${STYLES_FOLDER} \
             ${SCRIPTS_FOLDER} && \
    \
    chown -R ${USER_NAME}: ${CODE_FOLDER} \
                           ${RESOURCES_FOLDER} \
                           ${ASSETS_FOLDER} \
                           ${STYLES_FOLDER} \
                           ${SCRIPTS_FOLDER}

USER node
WORKDIR ${CODE_FOLDER}
COPY --chown=node code ${CODE_FOLDER}
