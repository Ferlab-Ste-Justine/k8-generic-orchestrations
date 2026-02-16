# Polaris Service Template

This folder provides Kubernetes templates for deploying Polaris as a service.

## Datasource configuration

Polaris requires an SQL database (e.g., PostgreSQL, MySQL) to persist information.  
Note: The database itself is not provisioned by these templates—you are responsible for creating and managing it.

To connect polaris to your database, add the following environment variables to the `env` section of the `polaris` container in the deployment resource:
- `QUARKUS_DATASOURCE_USERNAME`: Database username
- `QUARKUS_DATASOURCE_PASSWORD`: Database password
- `QUARKUS_DATASOURCE_JDBC_URL`: JDBC connection string (e.g., `jdbc:postgresql://your-db-host:5432/your-db-name`)

## AWS configuration

The templates assume data will be stored in S3 or MinIO.  
Add the following environment variables to the `env` section of the `polaris` container in the `polaris` deployment resource:
- AWS_REGION
- AWS_ACCESS_KEY_ID
- AWS_SECRET_KEY
- AWS_ENDPOINT_URL


## Authentication configuration and application.properties

The polaris ConfigMap resource injects the application.properties file described in the Polaris documentation.
 
You can use the provided configuration as is, or overwrite it downstream to suit your needs.
By default, it assumes the use of the internal token broker with symmetric-key credentials (i.e., username and password) for authentication.

To use this default setup, add the following environment variables to the env section of the polaris container in your deployment. These variables are referenced in the application.properties file:

- `POLARIS_AUTHENTICATION_TOKEN_BROKER_SYMMETRIC_KEY_SECRET`: Password for the global Polaris cross-realm user.
- `POLARIS_REALM_CONTEXT_REALMS`: Comma-separated list of realms to use.

Warning:
Not all Polaris clients support multiple realms. If you specify more than one realm in POLARIS_REALMS, ensure that all your clients are compatible with this configuration.
