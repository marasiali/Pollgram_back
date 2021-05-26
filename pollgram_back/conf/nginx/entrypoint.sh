#!/usr/bin/env sh
set -eu
envsubst '$DEPLOY_PORT' < /tmp/default-raw.conf > /etc/nginx/conf.d/default.conf
exec "$@"