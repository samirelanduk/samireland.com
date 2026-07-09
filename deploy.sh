set -e

HOSTNAME=samireland.com
TAG=prod
NEXT_PUBLIC_ALLOW_FALLBACK="false"

# Calculate environment variables
export BACKEND_URL=https://$HOSTNAME/api
export FRONTEND_URL=https://$HOSTNAME
export MEDIA_URL=https://$HOSTNAME
export BUILD_API_URL=https://$HOSTNAME/api
export NEXT_PUBLIC_API_URL=https://$HOSTNAME/api
export DOCS_HOSTNAME=docs.$HOSTNAME

# Build backend and nginx images
export DOCKER_DEFAULT_PLATFORM=linux/amd64
TAG=$TAG docker compose -f docker-compose.yml -p sidc build django nginx docs

# Push backend and nginx images
TAG=$TAG docker compose -f docker-compose.yml -p sidc push django nginx docs

# Create directory if it doesn't exist
ssh $HOSTNAME "mkdir -p ~/$HOSTNAME"

# Send compose files and secrets
scp docker-compose.yml $HOSTNAME:~/$HOSTNAME/docker-compose.yml
scp docker-compose.prod.yml $HOSTNAME:~/$HOSTNAME/docker-compose.prod.yml
scp secrets.env $HOSTNAME:~/$HOSTNAME/secrets.env

# Pull backend and nginx images
ssh $HOSTNAME "cd ~/$HOSTNAME && TAG=$TAG docker compose -p sidc pull django nginx docs"

# Define env block
ENV_BLOCK="BACKEND_URL=$BACKEND_URL FRONTEND_URL=$FRONTEND_URL MEDIA_URL=$MEDIA_URL BUILD_API_URL=$BUILD_API_URL NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL TAG=$TAG HOSTNAME=$HOSTNAME DOCS_HOSTNAME=$DOCS_HOSTNAME NEXT_PUBLIC_ALLOW_FALLBACK=$NEXT_PUBLIC_ALLOW_FALLBACK"

# Start all services apart from next
ssh $HOSTNAME "cd ~/$HOSTNAME && $ENV_BLOCK docker compose -p sidc -f docker-compose.yml -f docker-compose.prod.yml up -d postgres pgbackups upgrade collectstatic django nginx docs"

# Connect to bridge network
ssh $HOSTNAME 'docker network inspect bridge -f "{{range .Containers}}{{.Name}} {{end}}" | grep -qw sidc_nginx || docker network connect bridge sidc_nginx'
ssh $HOSTNAME 'docker network inspect bridge -f "{{range .Containers}}{{.Name}} {{end}}" | grep -qw sidc_docs || docker network connect bridge sidc_docs'

# Build next
TAG=$TAG docker compose -f docker-compose.yml -p sidc build next

# Push next image
TAG=$TAG docker compose -f docker-compose.yml -p sidc push next

# Pull next image
ssh $HOSTNAME "cd ~/$HOSTNAME && TAG=$TAG docker compose -p sidc pull next"

# Start next
ssh $HOSTNAME "cd ~/$HOSTNAME && $ENV_BLOCK docker compose -p sidc -f docker-compose.yml -f docker-compose.prod.yml up -d next"