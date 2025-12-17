# About

Phenovar is a private codebase hosted outside of Ferlab that we are operating.

For docker image and documentation about the service work flow and contracts (in particular, the meaning of various environment variables), see: https://github.com/Ferlab-Ste-Justine/phenovar

For local kubernetes troubleshoot deployement, see: https://github.com/Ferlab-Ste-Justine/kvm-dev-orchestrations/tree/main/kubernetes-orchestrations/phenovar

# Quick Architectural Note

The Celery worker which essentially runs the phenovar ETL is currently orchestrated with the phenovar service which will always be up.

As the celery worker has needed a modest 8GB of RAM to run in the proof on concept, it was deemed acceptable.

However, if it balloons to much bigger requirements than this on actual data, it will make sense to spend more time to ajust this solution to run the celery worker handling the job in the same pod as the client making the phenovar api call, that way it will be transient for the duration of the job only and significant amounts of RAM won't be wasted.

One gotcha to be aware of here, however, is that phenovar appears to have issues running several requests concurrently (haven't yet confirmed the problem for different request bodies, but it was observed if you run the same request body twice with the second one before the first job finished on several celery workers) so in the case where the celery worker lives with the client making the request, we will have to spend additional time analysing and managing any concurrency issues.

# Requirement notes

For environment variables and volumes, we probably passed more than really needed to some service (ex: flower server) as we did not invest the time needed to determine the strict minimum that various services required (what are are recommending in this documentation is an upper bound of things to provide to guarantee functionality based on empirical observations).

If you think that some are not needed for certain services, you are welcome to spend the time to validate your assessment and then make the necessary adjustments.