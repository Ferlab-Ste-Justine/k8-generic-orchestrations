#!/bin/sh
set -euo pipefail

: "${POLARIS_MGMT_SERVICE_URL:? POLARIS_MGMT_SERVICE_URL environment variable is required}"


echo "Waiting for Polaris to be available"

until curl -sf $POLARIS_MGMT_SERVICE_URL/q/health/ready > /dev/null; do
  echo "Polaris is not available yet. Retrying in 5 seconds..."
  sleep 5
done

echo "Polaris is available. Proceeding with catalog initialization."
