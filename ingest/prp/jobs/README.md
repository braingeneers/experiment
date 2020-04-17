# Why run Kubernetes jobs?

If someone has an amazing new analysis that they want to use on the data, they have to recreate the same analysis on each new data set. They could give me their analysis to automate into ingest, but then I would have to take the time to understand the analysis in order to correctly and efficiently automate it, while also downloading the right packages. With the kubernetes jobs, one can automatically upload the analysis they want done and then have it done with all subsequent data sets. 

## Set Up Docker
If you will need to run an analysis task after ingest you will just commit your `.yaml` file to the experiments repo under `ingest/prp/jobs` and it will be run automatically.
If your analysis task has some dependency on another analysis task running first, there's a trick in the `.yaml` files to running a series of containers sequentially using `initContainer`. There's an example of it in the example job `job_sequential_example.yaml`. So anyone that has such a requirement will have to define all the jobs that run in series in one yaml file, everyone else just adds their own yaml file as with the example `job_independent_example.yaml`. All .yaml files can use a single variable `${UUID}` in the yaml and that will be replaced with the `UUID` of the experiment being uploaded. Everything else should be pulled from PRP/S3 at runtime, and results should be added back to PRP/S3, and if appropriate a UI on `braingeneers.gi.ucsc.edu/dashboard` can present the results from S3.

