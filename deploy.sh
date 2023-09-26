#!/bin/bash

# Check minimum number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: ./local.sh DOMAIN [--allowfallback] [--proxy=CONTAINER_NAME]"
    exit 1
fi

export TAG=prod
export NEXT_PUBLIC_ALLOW_FALLBACK="false"
export HOSTNAME=$1
export DOCS_HOSTNAME=docs.$1
PROXY_CONTAINER="proxy"

# Shift past the first argument
shift

# Parse optional arguments
while (( "$#" )); do
  case "$1" in
    --allowfallback)
      export NEXT_PUBLIC_ALLOW_FALLBACK="true"
      shift
      ;;
    --proxy=*)
      PROXY_CONTAINER="${1#*=}" # Extract value after the "="
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./local.sh DOMAIN [--allowfallback] [--proxy=CONTAINER_NAME]"
      exit 1
      ;;
  esac
done

export BACKEND_URL=https://$HOSTNAME/api
export FRONTEND_URL=https://$HOSTNAME

export MEDIA_URL=https://$HOSTNAME
export BUILD_API_URL=https://$HOSTNAME/api
export NEXT_PUBLIC_API_URL=https://$HOSTNAME/api

docker compose -f docker-compose.yml -p sidc build next --progress=plain --no-cache && \
    docker compose -f docker-compose.yml -p sidc build && \
    docker compose -f docker-compose.yml -p sidc push && \
    ssh $HOSTNAME "mkdir -p ~/$HOSTNAME" && \
    scp docker-compose.yml $HOSTNAME:~/$HOSTNAME/docker-compose.yml && \
    scp secrets.env $HOSTNAME:~/$HOSTNAME/secrets.env && \
    ssh $HOSTNAME "cd ~/$HOSTNAME && BACKEND_URL=$BACKEND_URL FRONTEND_URL=$FRONTEND_URL MEDIA_URL=$MEDIA_URL BUILD_API_URL=$BUILD_API_URL NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL TAG=$TAG HOSTNAME=$HOSTNAME DOCS_HOSTNAME=$DOCS_HOSTNAME NEXT_PUBLIC_ALLOW_FALLBACK=$NEXT_PUBLIC_ALLOW_FALLBACK docker compose -p sidc pull" && \
    ssh $HOSTNAME "cd ~/$HOSTNAME && BACKEND_URL=$BACKEND_URL FRONTEND_URL=$FRONTEND_URL MEDIA_URL=$MEDIA_URL BUILD_API_URL=$BUILD_API_URL NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL TAG=$TAG HOSTNAME=$HOSTNAME DOCS_HOSTNAME=$DOCS_HOSTNAME NEXT_PUBLIC_ALLOW_FALLBACK=$NEXT_PUBLIC_ALLOW_FALLBACK docker compose -p sidc up -d" && \
    ssh $HOSTNAME "docker network connect bridge sidc_nginx" && \
    ssh $HOSTNAME "docker network connect bridge sidc_docs" && \
    ssh $HOSTNAME "docker restart $PROXY_CONTAINER"