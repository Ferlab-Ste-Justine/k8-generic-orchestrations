# About

These manifests are to deploy aidbox on a kubernetes cluster.

# Prerequisites

You need a postgres database accessible via the **aidbox-db** endpoint.

Its credentials should be stored in a secret structured like so:

```
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: aidbox-db-credentials
data:
  password: ...
  username: ...
```

# Usage Note

If nothing else, you probably want to **kustomize** the secret. All its values are set to **kustomizeMe**

# Planned Improvements

An ingress resource using a certificate for external access will be added in the future