# About

This cron job constantly updates a kubernetes secret with a generated phenovar token.

The token is generated in an init container and a main container upserts the value in a kubernetes secret.

# Orchestrations

## service-account

Provides a service account with minimal permission complementary role and role-binding to do the task.

The namespace should be specified downstream.

## cron-job

### Expected Kustomize extensions

The **token-generation** init container expects the following environment variables to be added to the init container generating the token:
  - S3_ENDPOINT
  - S3_BUCKET
  - S3_ACCESS_KEY
  - S3_SECRET_KEY
  - SGMADMIN_PASSWORD
  - DJANGO_SUPERUSER_USERNAME
  - DJANGO_SUPERUSER_PASSWORD
  - DJANGO_SUPERUSER_EMAIL

It also expects image pull secrets to be added to the pod (as the phenovar image used for the init container is private).

The **phenovar-token-upsert** main container expects the following environment variable to be defined: **PHENOVAR_NAMESPACE**.

You can also optionally define the **PHENOVAR_TOKEN_SECRET** environment variable to change the secret name (defaults to **phenovar-token**).