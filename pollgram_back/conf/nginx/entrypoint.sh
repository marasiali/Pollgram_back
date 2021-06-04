#!/usr/bin/env sh
set -eu

if [ "$DEPLOY_PORT" -ne "80" ]; then
   export DEPLOY_PORT_COLON=":${DEPLOY_PORT}"
fi

envsubst '$DEPLOY_PORT_COLON' < /tmp/default-raw.conf > /etc/nginx/conf.d/default.conf
exec "$@"