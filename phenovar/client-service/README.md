# Expected Kustomize extensions

The client service provides a template with an init container that generates a phenovar token on path /opt/phenovar-token/token.

It expects you to define the main container of the service that will run as well as a shared volume for path /opt/phenovar-token/token on the init container and the container you will define (presumably an in memory emptydir, but up to the user).

It expects image pull secrets to be added to the pod (as the phenovar image used for the init container is private).

It expects the following environment variables to be added to the init container generating the token:
  - S3_ENDPOINT
  - S3_BUCKET
  - S3_ACCESS_KEY
  - S3_SECRET_KEY
  - SGMADMIN_PASSWORD
  - DJANGO_SUPERUSER_USERNAME
  - DJANGO_SUPERUSER_PASSWORD
  - DJANGO_SUPERUSER_EMAIL