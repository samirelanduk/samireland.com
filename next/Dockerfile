# Step 1: Build the Next.js application
FROM node:current-alpine AS builder

WORKDIR /app

# Copy package.json and package-lock.json before other files
# Utilize Docker cache to save re-installing dependencies if unchanged
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all files
COPY . .

# Build application
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_MEDIA_URL
ARG NEXT_PUBLIC_ALLOW_FALLBACK
RUN NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_PUBLIC_MEDIA_URL=$NEXT_PUBLIC_MEDIA_URL \
    NEXT_PUBLIC_ALLOW_FALLBACK=$NEXT_PUBLIC_ALLOW_FALLBACK \
    npm run build

# Step 2: Serve Next.js app via a Node.js server
FROM --platform=amd64 node:current-alpine

WORKDIR /app

# Copy over dependencies and build output from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Set environment to production
ENV NODE_ENV production

# Expose the listening port
EXPOSE 3000

# Run your production server
CMD ["npm", "start"]