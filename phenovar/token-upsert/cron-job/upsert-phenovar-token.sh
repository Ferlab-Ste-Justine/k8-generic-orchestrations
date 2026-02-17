#!/bin/sh

set -e

: "${PHENOVAR_TOKEN_PATH:=/opt/phenovar-token/token}"
: "${PHENOVAR_TOKEN_SECRET:=phenovar-token}"
: "${PHENOVAR_NAMESPACE:=default}"

if [ ! -f "${PHENOVAR_TOKEN_PATH}" ]; then
  echo "Phenovar token file not found at path ${PHENOVAR_TOKEN_PATH}"
fi

TOKEN=$(cat $PHENOVAR_TOKEN_PATH)
TOKEN="${TOKEN%%*[[:blank:]]}"

echo "Upserting phenovar token in secret '$PHENOVAR_TOKEN_SECRET' of namespace '$PHENOVAR_NAMESPACE'";

kubectl -n $PHENOVAR_NAMESPACE create secret generic $PHENOVAR_TOKEN_SECRET \
  --from-literal=token="${TOKEN}" \
  --dry-run=client \
  -o yaml \
  | kubectl -n $PHENOVAR_NAMESPACE apply -f -