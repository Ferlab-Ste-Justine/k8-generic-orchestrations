# Expected Kustomize extensions

The service expects image pull secrets to be added to the pod (as the phenovar image used for most of the containers in the pod is private).

The service expects the following volumes:
  - A volume for phenovar results mounted at the path **/opt/phenovar/data** of the celery worker and phenovar server
  - A volume for phenovar resources mounted at the path **/opt/phenovar/resources** of the celery worker, phenovar server and flower server
  - An optional volume containing your S3 CA (if you use an internal CA) mounted at whichever directory an **S3_CA_PATH** environment variable (pointing to the S3 CA path) defines. This is for the celery worker, phenovar server and flower server

The **create-databases** init container expects the same environment variables as the **create-databases** job.

The **phenovar-server**, **celery-worker** and **flower-server** containers expect the following environment variables:
  - SGMADMIN_PASSWORD
  - DJANGO_SUPERUSER_USERNAME
  - DJANGO_SUPERUSER_PASSWORD
  - DJANGO_SUPERUSER_EMAIL
  - PHENOVAR_PROXY_PORT
  - PHENOVAR_PROXY_PROTOCOL
  - PHENOVAR_PROXY_DOMAIN

Additionally, ingresses will have to be defined for the phenovar server and flower server to be externally accessible (don't forget to put a basic auth in front of the flower server). Rather than elaborate the exact requirements for those, see: https://github.com/Ferlab-Ste-Justine/kvm-dev-orchestrations/tree/main/kubernetes-orchestrations/phenovar/service/service/ingress.yml

# Requisite RAM note

On a poc with dummy data, we determined that the celery worker needed 8GB of RAM to do its job.

You may find that you need more on actual data and if you notice this, you should ajust this template to reflect actual requirements.