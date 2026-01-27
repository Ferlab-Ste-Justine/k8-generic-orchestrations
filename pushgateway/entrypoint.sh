#! /bin/sh

if [ "$PUSHGATEWAY_PERMANENT_STORAGE" = "true" ]; then
  PERSISTENCE_ARG="--persistence.file=/var/lib/pushgateway/state"
fi

if [ "$PUSHGATEWAY_USE_TLS" = "true" ]; then
  CONFIG_ARG="--web.config.file=/etc/pushgateway/config/config.yml"
fi

exec pushgateway \
    ${PERSISTENCE_ARG:+$PERSISTENCE_ARG} \
    ${CONFIG_ARG:+$CONFIG_ARG} \
    --web.listen-address=0.0.0.0:9091