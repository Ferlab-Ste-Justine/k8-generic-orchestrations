# About

This is a kustomization to orchestrate an a high availability keycloak service.

# Requirements

## Postgres

It is assumed that a postgres service called **keycloak-db** has already been setup.

A database named **keycloak** should exist in your postgres instance accessible with credentials stored in a secret named **keycloak-db-credentials** with the keys of **username** and **password**. 

## Admin Password

The keycloak admin credentials should be stored in a secret called **keycloak-credentials** with the keys of **username** and **password**

# Usage

## Keycloak Orchestration Generation

The keycloak orchestration file is generated from the **codecentric** **keycloak** Helm chart which can be found here: https://github.com/codecentric/helm-charts

To generate it, you need to run the following once:

```
helm repo add codecentric https://codecentric.github.io/helm-charts
```

After that, you can execute the **generate.sh** script to generate it.

**The generated file has been commited to version control for convenience given that updates to it should be uncommon, so if you do not need to update it, you can ignore this step.**

## Kustomization

The keycloak orchestration can be applied as is.

An external method to access keycloak is left to the consumer of this kustomization to implement.

For a local environment, a nodeport should do. For a more serious environment, you'll probably want an ingress.