# Expected Kustomize extensions

This job downloads the phenovar genomic libraries from an S3 store to a kubernetes volume (as phenovar expects its genomic libraries to be on a filesystem).

The job expects an rclone configuration volume containing an **rclone.conf** file passed at the path **/etc/rclone/**. Related to this, the job expects an **S3_CONF_NAME** environment variable containing the name of the s3 configuration in your **rclone.conf** file that the job will use to download the phenovar genomic libraries from your s3 store.

The job also expects and **S3_PATH** environment variable containing an s3 path (starting with the bucket name) to the phenovar resources to rclone.

If your S3 store uses an internal CA, it expects an **S3_CA_PATH** environment variable to define where the CA is and for the CA cert to be mounted at that path.

And finally, it expects the kubernetes volume that will contain your phenovar resources to be mounted with write access at the path **/var/lib/phenovar-resources**.