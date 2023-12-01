# About

This is a kustomization to orchestrate a prometheus service.

# Usage

## Prometheus Orchestration Generation

The prometheus crds files are generated from the **prometheus-operator** GitHub repository which can be found here: https://github.com/prometheus-operator/prometheus-operator

The prometheus orchestration file is generated from the **prometheus-community** **kube-prometheus-stack** Helm chart which can be found here: https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

The prometheus kustomization file is generated listing the crds and orchestration files as resources.

To generate all of this, you need to run the following:

```
./generate.sh
```

**The generated files have been commited to version control for convenience given that updates to it should be uncommon, so if you do not need to update them, you can ignore this step.**

## Kustomization

The prometheus orchestration can be applied running the following:

```
kubectl apply -k . --server-side
```

An external method to access prometheus is left to the consumer of this kustomization to implement.

For a local environment, a nodeport should do. For a more serious environment, you'll probably want an ingress.
