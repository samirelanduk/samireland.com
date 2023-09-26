FROM --platform=linux/amd64 nginx:1.19.0-alpine

ARG CONF_NAME=nginx.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY ${CONF_NAME} /etc/nginx/conf.d