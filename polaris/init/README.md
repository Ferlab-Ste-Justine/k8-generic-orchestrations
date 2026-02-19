# Polaris initialization templates

This folder provides templates for initializing resources on an existing Polaris server.

The templates assume:
- Authentication is handled via the internal token broker using symmetric key credentials (username and password).
- All catalogs are stored on the same S3/MinIO account and share a common S3 endpoint.

Initialization is performed in 3 steps, each managed by a separate container (two init containers and the main container).
Configuration is provided via environment variables and configmap as described below.

**Note**:
While multiple realms are supported by this initialization process, not all polaris clients are compatible with multi-realm configurations. Please verify client compatibility before using multiple realms.


## Step1 1: wait-for-polaris init container

This step ensures that the polaris service is ready before proceeding.

Set the following environment variable in the wait-for-polaris init container of the polaris-init-job:

- `POLARIS_MGMT_SERVICE_URL`: The URL of the Polaris management service, used to verify service readiness. Defaults to `http://polaris-mgmt:8182`.

## Step 2: bootstrap-realms init container

In the `bootstrap-realms` init container of the `polaris-init-job`, add the following environment variables:

- `QUARKUS_DATASOURCE_USERNAME`: Polaris database username
- `QUARKUS_DATASOURCE_PASSWORD`: Polaris database password
- `QUARKUS_DATASOURCE_JDBC_URL`: Polaris database JDBC URL (e.g., `jdbc:postgresql://my-db-host:5432/my-db-host`)
- `POLARIS_REALM_NAMES`: Comma-separated list of realms to create (e.g., `realm1,realm2`)

For each realm listed in `POLARIS_REALM_NAMES`, also add:
- `POLARIS_REALM_<REALM NAME>_ROOT_USER`: Realm root principal username (polaris client ID)
- `POLARIS_REALM_<REALM NAME>_ROOT_PASSWORD`: Realm root principal password (polaris client secret)

## Step 3: init-polaris container

Create a ConfigMap named `polaris-realm-config` with a key `realm-config.json`.

This file will be mounted into the `polaris-init-job` container.  
An example `realm-config.json` is provided in this folder.

In `realm-config.json`, specify for each realm the catalogs, principals, roles, and namespaces to create.

In the `init-polaris` container of the `polaris-init-job`, add the following environment variables:

For each realm in your `realm-config.json`:
- `POLARIS_REALM_<REALM NAME>_ROOT_USER`: Realm root principal username
- `POLARIS_REALM_<REALM NAME>_ROOT_PASSWORD`: Realm root principal password

For each principal to create (as specified in `realm-config.json`):
- `POLARIS_REALM_<REALM NAME>_<PRINCIPAL NAME>_USER`: Principal username
- `POLARIS_REALM_<REALM NAME>_<PRINCIPAL NAME>_PASSWORD`: Principal password
  
Finally, add:
- `CATALOG_ENDPOINT`: S3 endpoint URL to use for the catalogs
- `POLARIS_SERVICE_HOST`: host for the polaris service, default to `polaris:8181`