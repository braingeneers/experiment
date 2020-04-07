#!/bin/bash
# Runs all jobs in inbox/jobs, see documentation at https://github.com/braingeneers/inbox

for JOB_YAML in jobs/*.yaml; do
    echo "Running ${JOB_YAML}"
    envsubst < ${JOB_YAML} | kubectl create -f -
done

