# keycloak

Generic Keycloak 26 (Quarkus) deployment template for Kubernetes. Designed
to be used as a kustomize base with environment-specific overlays.

## What it deploys

- **Deployment** — 2 replicas, hard pod anti-affinity (different nodes), Quarkus
  runtime with `kc.sh build && kc.sh start --optimized`.
- **Service** — ClusterIP on port 80 with `sessionAffinity: ClientIP` for
  smooth multi-replica auth flows.
- **Service (headless)** — Used by JGroups DNS_PING for Infinispan session
  replication across replicas.

## Prerequisites

Two secrets must exist in the target namespace before applying:

| Secret | Keys | Purpose |
|---|---|---|
| `keycloak-db` | `host`, `password` | PostgreSQL connection |
| `keycloak-admin` | `username`, `password` | Bootstrap admin account |

`KC_DB_URL_DATABASE` defaults to `keycloak` and `KC_DB_USERNAME` to `keycloak`.
Override via a kustomize patch if your setup differs.

## What environments must provide as overlays

- `KC_HOSTNAME` — public URL of the Keycloak instance (required for production)
- Image — override `quay.io/keycloak/keycloak:26.1` with your registry/version
- Ingress — environment-specific ingress/load-balancer configuration
- ServiceAccount — only needed if the platform requires one (e.g. AWS EKS Pod
  Identity for IAM permissions). Most environments can omit it.
- Node scheduling constraints — `nodeSelector`, tolerations, etc.

## Why Deployment and not StatefulSet

Keycloak's session state lives in the Infinispan distributed cache (replicated
across pods via JGroups), not in pod-local storage. There are no persistent
volumes to manage per-pod. A Deployment with hard anti-affinity gives the same
HA guarantees with less operational complexity.

## Command explained

```
/opt/keycloak/bin/kc.sh build && exec /opt/keycloak/bin/kc.sh start --optimized
```

`kc.sh build` runs the Quarkus augmentation step at pod start — it bakes
build-time options (DB type, health/metrics) into compiled artifacts.
`kc.sh start --optimized` then starts the server using those artifacts,
skipping re-augmentation for a faster boot. `exec` replaces the shell so
kubelet SIGTERM reaches `kc.sh` directly for a clean graceful shutdown.