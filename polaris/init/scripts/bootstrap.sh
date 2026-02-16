#!/bin/sh
set -euo pipefail

: "${POLARIS_REALM_NAMES:?Environment variable POLARIS_REALM_NAMES is required (comma-separated)}"

create_realm_if_not_exists() {
  local realm="$1"
  local client_id="$2"
  local client_secret="$3"
  
  echo "Creating realm $realm"
  local output=$(java -jar /deployments/polaris-admin-tool.jar bootstrap -r "$realm" -c "$realm,$client_id,$client_secret" -p 2>&1)
  local status=$?
  if echo "$output" | grep -q "It appears this metastore manager has already been bootstrapped"; then
      echo "Realm already bootstrapped for realm ${realm}"
  fi
  if [ $status -ne 0 ]; then
      echo "❌ Unexpected error during bootstrap"
      echo "$output"
      exit 1
  fi
  echo "Done creating realm $realm"
}

main() {
  echo "create realms if not exists"
  local realms
  local users
  local passwords
  IFS=',' read -r -a realms <<< "$POLARIS_REALM_NAMES"

  for idx in "${!realms[@]}"; do
    local realm="${realms[$idx]}"
    local realm_upper=$(echo "$realm" | tr '[:lower:]' '[:upper:]')
    local env_user_var="POLARIS_REALM_${realm_upper}_ROOT_USER"
    local env_password_var="POLARIS_REALM_${realm_upper}_ROOT_PASSWORD"
    eval "client_id=\${$env_user_var}"
    eval "client_secret=\${$env_password_var}"
    if [ -z "$client_id" ] || [ -z "$client_secret" ]; then
      echo "❌ Missing credentials for realm '$realm'. Expected env vars: $env_user_var and $env_password_var"
      exit 1
    fi
    create_realm_if_not_exists "${realm}" "${client_id}" "${client_secret}"
  done
}

main