# Ingest workflow

There's a simple way to handle the automatic deployment of analysis tasks to the PRP after the `/inbox` ingest process runs which should cover the basic use cases we have for workflow management. There are 2 example jobs and a simple script in this repo that demonstrate the process of creating a new analysis task to run after the ingest process.

## Basic usage:
If you will need to run an analysis task after ingest you will just commit your `.yaml` file to the experiments repo under `ingest/prp/jobs` and it will be run automatically.
If your analysis task has some dependency on another analysis task running first, there's a trick in the `.yaml` files to running a series of containers sequentially using `initContainer`. There's an example of it in the example job `job_sequential_example.yaml`. So anyone that has such a requirement will have to define all the jobs that run in series in one yaml file, everyone else just adds their own yaml file as with the example `job_independent_example.yaml`. All .yaml files can use a single variable `${UUID}` in the yaml and that will be replaced with the `UUID` of the experiment being uploaded. Everything else should be pulled from PRP/S3 at runtime, and results should be added back to PRP/S3, and if appropriate a UI on `braingeneers.gi.ucsc.edu/dashboard` can present the results from S3.

## Details:
The jobs will show up in the namespace while running and remain there for only 90 seconds after the job finishes (configurable in the `.yaml`). Note that if you need to get the logs in a job that has a sequence of containers you need to add `-c CONTAINER_NAME` as in `kubectl get logs PODNAME -c CONTAINER_NAME`. A dedicated user has been added to our namespace to deploy the jobs. That file is stored as a kubernetes secret under `kube-config`. The ingest process will run the script `run_jobs.sh` which simply creates jobs for all the files in `experiment/ingest/prp/jobs`.
I'm sure there will be some details to flush out as we go. Currently I'm assuming an analysis task can check if it should execute or not (a simple S3 query) and exit if it's not needed for a particular ingest. That's simple enough, but perhaps in the future we'll make that more robust.