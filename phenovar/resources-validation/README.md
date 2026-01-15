# Expected Kustomize extensions

This job verifies the integrity of phenovar genomic libraries using a pre-computed hash list already present in the container image which was computed from a known valid copy.

The job expects the kubernetes volume that will contain your phenovar resources to be mounted with write access at the path **/var/lib/phenovar-resources**.