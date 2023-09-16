#!/bin/bash

# Check minimum number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: ./local.sh PORT_NUMBER [--allowfallback]"
    exit 1
fi

export TAG=local
export PORT=$1
export NEXT_PUBLIC_ALLOW_FALLBACK="false"

# Shift past the first argument
shift

# Parse optional arguments
while (( "$#" )); do
  case "$1" in
    --allowfallback)
      export NEXT_PUBLIC_ALLOW_FALLBACK="true"
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./local.sh PORT_NUMBER [--allowfallback]"
      exit 1
      ;;
  esac
done

export BACKEND_URL=http://localhost:$PORT/api
export FRONTEND_URL=http://localhost:$PORT

export MEDIA_URL=http://localhost:$PORT
export BUILD_API_URL=http://host.docker.internal:9012/api
export NEXT_PUBLIC_API_URL=http://sidc_django
export HOSTNAME=localhost

docker compose -f docker-compose.yml -f docker-compose.dev.yml -p sidc build next --progress=plain --no-cache && \
    docker compose -f docker-compose.yml -f docker-compose.dev.yml -p sidc build && \
    docker compose -f docker-compose.yml -f docker-compose.dev.yml -p sidc down && \
    docker compose -f docker-compose.yml -f docker-compose.dev.yml -p sidc up -d