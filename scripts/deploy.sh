#!/usr/bin/env bash

###
export PROJECT_NAME='vash'
export PROJECT_URL='https://github.com/vsevolod-skripnik/vash.git'
export USER="$(whoami)"
export SSHPASS="${PRODUCTION_SERVER_PASSWORD}"
###


# Shortcuts to interact with production

alias run_on_production='sshpass -e ssh ${PRODUCTION_SERVER_USERNAME}@${PRODUCTION_SERVER_HOST}'
shopt -s expand_aliases
ssh-keyscan -t rsa ${PRODUCTION_SERVER_HOST} > ~/.ssh/known_hosts

function send_to_production {
  sshpass -e scp $1 ${PRODUCTION_SERVER_USERNAME}@${PRODUCTION_SERVER_HOST}:$2
}

function download_from_production {
  sshpass -e scp ${PRODUCTION_SERVER_USERNAME}@${PRODUCTION_SERVER_HOST}:$1 $2
}


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


# Different variables

export PRODUCTION_ENVIRONMENT_FILE="${PRODUCTION_ENVIRONMENT_ROOT}/${PROJECT_NAME}.env"
export COMMIT=$(echo ${TRAVIS_COMMIT:0:7})  # Shorten commit hash
export STATIC_TARBALL_NAME="${COMMIT}.tar.gz"


# Variables to run local project

export PRODUCTION_USER_ID="$(run_on_production 'id -u')"
export HOST_USER_ID="${PRODUCTION_USER_ID}"
export MEDIA_DIRECTORY="${TRAVIS_BUILD_DIR}/resources/media"
export STATIC_DIRECTORY="${TRAVIS_BUILD_DIR}/resources/static"
export CERTIFICATES_DIRECTORY="${TRAVIS_BUILD_DIR}/resources/certificates"


# Variables to run project on production

export PRODUCTION_STATIC_DIRECTORY="${PRODUCTION_ARTEFACTS_STATIC_DIRECTORY}/${COMMIT}"
export PRODUCTION_REPOSITORY_DIRECTORY="${PRODUCTION_REPOSITORIES_DIRECTORY}/${COMMIT}"


# Docker image names

export DOCKER_NGINX_IMAGE="${PROJECT_NAME}_nginx:${COMMIT}"
export DOCKER_NGINX_IMAGE_FILE="${COMMIT}.tar"

export DOCKER_DJANGO_IMAGE="${PROJECT_NAME}_django:${COMMIT}"
export DOCKER_DJANGO_IMAGE_FILE="${COMMIT}.tar"

docker_postgres_image_line=`cat .env | grep DOCKER_POSTGRES_IMAGE`
export DOCKER_POSTGRES_IMAGE="${docker_postgres_image_line/DOCKER_POSTGRES_IMAGE=/}"
export DOCKER_POSTGRES_IMAGE_FILE="${DOCKER_POSTGRES_IMAGE/:/_}.tar"


# Local Postgres

export POSTGRES_USERNAME="${PROJECT_NAME}"
export POSTGRES_DATABASE="${PROJECT_NAME}"
export POSTGRES_BACKUP_NAME='backup.sql'
export POSTGRES_BACKUP_PATH="/tmp/${POSTGRES_BACKUP_NAME}"
export POSTGRES_CONTAINER="${PROJECT_NAME}_postgres_1"
export POSTGRES_ARTEFACT_NAME="${COMMIT}.sql"
export POSTGRES_ARTEFACT_PATH="/tmp/${POSTGRES_ARTEFACT_NAME}"


# Production Postgres

export PRODUCTION_POSTGRES_USERNAME="${PROJECT_NAME}"
export PRODUCTION_POSTGRES_DATABASE="${PROJECT_NAME}"
export PRODUCTION_POSTGRES_BACKUP_NAME="$(date +%d-%m-%y__%H-%M.sql)"
export PRODUCTION_POSTGRES_BACKUP_PATH="${PRODUCTION_BACKUPS_POSTGRES_DIRECTORY}/${PRODUCTION_POSTGRES_BACKUP_NAME}"


# Create directory structure on production

run_on_production "
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
"


# Read deployment state on production

if run_on_production "stat ${PRODUCTION_ENVIRONMENT_FILE} > /dev/null 2>&1"
then
  nginx_ports_set_current=$(run_on_production "cat ${PRODUCTION_ENVIRONMENT_FILE}" | grep NGINX_PORT_SET_CURRENT)
  nginx_ports_set_previous=$(run_on_production "cat ${PRODUCTION_ENVIRONMENT_FILE}" | grep NGINX_PORT_SET_PREVIOUS)
  export PRODUCTION_NGINX_PORT_SET_CURRENT="${nginx_ports_set_current/NGINX_PORT_SET_CURRENT=/}"
  export PRODUCTION_NGINX_PORT_SET_PREVIOUS="${nginx_ports_set_previous/NGINX_PORT_SET_PREVIOUS=/}"
  commit_current=$(run_on_production "cat ${PRODUCTION_ENVIRONMENT_FILE}" | grep COMMIT_CURRENT)
  commit_previous=$(run_on_production "cat ${PRODUCTION_ENVIRONMENT_FILE}" | grep COMMIT_PREVIOUS)
  export PRODUCTION_COMMIT_CURRENT="${commit_current/COMMIT_CURRENT=/}"
  export PRODUCTION_COMMIT_PREVIOUS="${commit_previous/COMMIT_PREVIOUS=/}"
else
  export PRODUCTION_NGINX_PORT_SET_CURRENT=
  export PRODUCTION_NGINX_PORT_SET_PREVIOUS=
  export PRODUCTION_COMMIT_CURRENT=
  export PRODUCTION_COMMIT_PREVIOUS=
fi


# Set permissions

sudo chown -R ${PRODUCTION_USER_ID}:${USER} .  # Stage and production user ids differ


# Build and run

docker-compose \
  -f compose/nginx.yml \
  -f compose/django.yml \
  -f compose/postgres.yml \
  -f compose/production.yml \
  -f compose/nginx_ports_A.yml \
  --project-directory . \
  up \
  -d \
  --build


# Download Postgres backup from production

run_on_production "
  docker exec ${PROJECT_NAME}${PRODUCTION_COMMIT_CURRENT}_postgres_1 \
    pg_dump \
      -U ${PRODUCTION_POSTGRES_USERNAME} \
      ${PRODUCTION_POSTGRES_DATABASE} \
  > ${PRODUCTION_POSTGRES_BACKUP_PATH}
"
download_from_production ${PRODUCTION_POSTGRES_BACKUP_PATH} ${POSTGRES_BACKUP_PATH}


# Wait for Postgres, load backup, and migrate

sleep 5s  # Give Postgres some time to boot

while [ "$( docker exec ${POSTGRES_CONTAINER} psql -U ${POSTGRES_USERNAME} -tAc "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DATABASE}'" )" != '1' ];
do echo 'Waiting for Postgres to create a database.'; sleep 5s; done

sleep 5s  # Give Postgres some time to restart after creating a database

until [[ "$( docker exec ${POSTGRES_CONTAINER} pg_isready )" ]];
do echo 'Waiting for Postgres to get ready.'; sleep 5s; done

docker cp ${POSTGRES_BACKUP_PATH} ${POSTGRES_CONTAINER}:/tmp
docker exec ${POSTGRES_CONTAINER} bash -c "psql -U ${POSTGRES_USERNAME} ${POSTGRES_DATABASE} < /tmp/${POSTGRES_BACKUP_NAME}" > /dev/null
docker exec ${PROJECT_NAME}_django_1 python manage.py migrate --noinput


# Collect static

sudo chown -R ${PRODUCTION_USER}:${USER} ${STATIC_DIRECTORY}
docker exec ${PROJECT_NAME}_django_1 python manage.py collectstatic --noinput


# Send images to production

function send_image_to_production {
  image_file=$1
  image_name=$2
  production_directory=$3
  image_path="/tmp/${image_file}"
  docker save -o ${image_path} ${image_name}
  send_to_production ${image_path} ${production_directory}
  run_on_production "docker load < ${production_directory}/${image_name}"
}

# send_image_to_production ${DOCKER_POSTGRES_IMAGE_FILE} ${DOCKER_POSTGRES_IMAGE} ${PRODUCTION_IMAGES_POSTGRES_DIRECTORY}
# send_image_to_production ${DOCKER_DJANGO_IMAGE_FILE} ${DOCKER_DJANGO_IMAGE} ${PRODUCTION_IMAGES_DJANGO_DIRECTORY}
# send_image_to_production ${DOCKER_NGINX_IMAGE_FILE} ${DOCKER_NGINX_IMAGE} ${PRODUCTION_IMAGES_NGINX_DIRECTORY}


# Send static to production

cd ${STATIC_DIRECTORY}
tar -zcf /tmp/${STATIC_TARBALL_NAME} .
cd -
send_to_production /tmp/${STATIC_TARBALL_NAME} /tmp/
run_on_production "
  mkdir -p ${PRODUCTION_STATIC_DIRECTORY}
  tar -zxf /tmp/${STATIC_TARBALL_NAME} -C ${PRODUCTION_STATIC_DIRECTORY}
  rm -rf /tmp/${STATIC_TARBALL_NAME}
"


# Send database to production

docker exec ${POSTGRES_CONTAINER} pg_dump -U ${POSTGRES_USERNAME} ${POSTGRES_DATABASE} > ${POSTGRES_ARTEFACT_PATH}
send_to_production ${POSTGRES_ARTEFACT_PATH} ${PRODUCTION_ARTEFACTS_POSTGRES_DIRECTORY}


# Clone project to another place to run second compose on production

run_on_production "
  cd ${PRODUCTION_REPOSITORIES_DIRECTORY}
  git clone ${PROJECT_URL} ${COMMIT}
  cd ${PRODUCTION_REPOSITORY_DIRECTORY}
  git checkout ${COMMIT}
  git reset --hard
"
