#!/usr/bin/env bash

export PROJECT_NAME='vash'


# Production directory structure

export PRODUCTION_ARTEFACTS_ROOT='~/artefacts'
export PRODUCTION_ARTEFACTS_DIRECTORY="${PRODUCTION_ARTEFACTS_ROOT}/${PROJECT_NAME}"
export PRODUCTION_ARTEFACTS_STATIC_DIRECTORY="${PRODUCTION_ARTEFACTS_DIRECTORY}/static"
export PRODUCTION_ARTEFACTS_POSTGRES_DIRECTORY="${PRODUCTION_ARTEFACTS_DIRECTORY}/postgres"

export PRODUCTION_BACKUPS_ROOT='~/backups'
export PRODUCTION_BACKUPS_DIRECTORY="${PRODUCTION_BACKUPS_ROOT}/${PROJECT_NAME}"
export PRODUCTION_BACKUPS_POSTGRES_DIRECTORY="${PRODUCTION_BACKUPS_DIRECTORY}/postgres"

export PRODUCTION_IMAGES_ROOT='~/images'
export PRODUCTION_IMAGES_DIRECTORY="${PRODUCTION_IMAGES_ROOT}/${PROJECT_NAME}"
export PRODUCTION_IMAGES_NGINX_DIRECTORY="${PRODUCTION_IMAGES_DIRECTORY}/nginx"
export PRODUCTION_IMAGES_DJANGO_DIRECTORY="${PRODUCTION_IMAGES_DIRECTORY}/django"
export PRODUCTION_IMAGES_POSTGRES_DIRECTORY="${PRODUCTION_IMAGES_DIRECTORY}/postgres"

export PRODUCTION_REPOSITORIES_ROOT='~/repositories'
export PRODUCTION_REPOSITORIES_DIRECTORY="${PRODUCTION_REPOSITORIES_ROOT}/${PROJECT_NAME}"

export PRODUCTION_RESOURCES_ROOT='~/resources'
export PRODUCTION_RESOURCES_DIRECTORY="${PRODUCTION_RESOURCES_ROOT}/${PROJECT_NAME}"
export PRODUCTION_RESOURCES_MEDIA_DIRECTORY="${PRODUCTION_RESOURCES_DIRECTORY}/media"
export PRODUCTION_RESOURCES_CERTIFICATES_DIRECTORY="${PRODUCTION_RESOURCES_DIRECTORY}/certificates"

export PRODUCTION_ENVIRONMENT_ROOT='~/environment'


# Functions

function create_directory_structure {
  mkdir -p ${PRODUCTION_ENVIRONMENT_ROOT}

  mkdir -p ${PRODUCTION_ARTEFACTS_ROOT} \
           ${PRODUCTION_ARTEFACTS_DIRECTORY} \
           ${PRODUCTION_ARTEFACTS_STATIC_DIRECTORY} \
           ${PRODUCTION_ARTEFACTS_POSTGRES_DIRECTORY}

  mkdir -p ${PRODUCTION_BACKUPS_ROOT} \
           ${PRODUCTION_BACKUPS_DIRECTORY} \
           ${PRODUCTION_BACKUPS_POSTGRES_DIRECTORY} \

  mkdir -p ${PRODUCTION_IMAGES_ROOT} \
           ${PRODUCTION_IMAGES_DIRECTORY} \
           ${PRODUCTION_IMAGES_NGINX_DIRECTORY} \
           ${PRODUCTION_IMAGES_DJANGO_DIRECTORY} \
           ${PRODUCTION_IMAGES_POSTGRES_DIRECTORY}

  mkdir -p ${PRODUCTION_REPOSITORIES_ROOT} \
           ${PRODUCTION_REPOSITORIES_DIRECTORY}

  mkdir -p ${PRODUCTION_RESOURCES_ROOT} \
           ${PRODUCTION_RESOURCES_DIRECTORY} \
           ${PRODUCTION_RESOURCES_MEDIA_DIRECTORY} \
           ${PRODUCTION_RESOURCES_CERTIFICATES_DIRECTORY}
}


# Main

export SSHPASS=${PRODUCTION_SERVER_PASSWORD}
ssh-keyscan -t rsa ${PRODUCTION_SERVER_HOST} > ~/.ssh/known_hosts
sshpass -e ssh ${PRODUCTION_SERVER_USERNAME}@${PRODUCTION_SERVER_HOST} "$(typeset -f); create_directory_structure"
