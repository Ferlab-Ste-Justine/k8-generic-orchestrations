# About

This is a kustomization to orchestrate an acme letsencrypt certificate.

Its requires **cert-manager** and **ingress-nginx** to be installed on your kubernetes cluster.

# Usage

You can either orchestrate a mock certificate to test your integration using the **staging** directory as your base or orchestrate a genuine certificate using the **genuine** directory as your base once you are confident that your orchestration work.

Either way, the format of your kustomization file should be similar:

kustomization.yml:
```
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- <path to this folder>/(staging|genuine)

patchesStrategicMerge:
- certificate.yml
- issuer.yml
```

certificate.yml:
```
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: letsencrypt[-staging]
spec:
spec:
  dnsNames:
  - <list your domains here>
  keyAlgorithm: <algorithm for your encryption key>
  keyEncoding: <encoding of your encryption key>
  keySize: <size of your encryption key>

```

issuer.yml:
```
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt[-staging]
spec:
  acme:
    email: <your contact email>
```