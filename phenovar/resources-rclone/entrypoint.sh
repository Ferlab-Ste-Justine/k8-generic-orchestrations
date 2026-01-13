#!/bin/sh

set -e

if [ -f $S3_CA_PATH ]; then 
  rclone sync --links --config "$RCLONE_CONF_PATH" --ca-cert $S3_CA_PATH "$S3_CONF_NAME:$S3_PATH" "$PHENOVAR_RESOURCES_DIR"
else 
  rclone sync --links --config "$RCLONE_CONF_PATH" "$S3_CONF_NAME:$S3_PATH" "$PHENOVAR_RESOURCES_DIR"
fi
