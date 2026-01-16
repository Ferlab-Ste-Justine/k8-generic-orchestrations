# Expected Kustomize extensions

This job wipes phenovar's volumes data, essentially wiping its entire state clean.

It expects phenovar services not to be running while it is running.

The following phenovar volumes should be mounted on the pod:
- Mysql at: /var/lib/phenovar-mysql
- Redis at: /var/lib/phenovar-redis
- Results at: /var/lib/phenovar-results