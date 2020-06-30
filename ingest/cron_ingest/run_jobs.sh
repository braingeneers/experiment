#!/bin/bash
# Runs all jobs in inbox/jobs, see documentation at https://github.com/braingeneers/experiment/tree/master/ingest/prp

if [ "$UUID" == "" ]
then
    echo "No feature containers are ran becasue there is no new batch."
elif [ "${UUID:11:1}" == "e" ]
then
    echo "Ephys feature containers are being prepared to run"
    for JOB_YAML in jobs/ephys/*.yaml; do
     #   kubectl delete job ${JOB_YAML}
        echo "Running ${JOB_YAML}"
        envsubst < ${JOB_YAML} | kubectl create -f -
    done
elif [ "${UUID:11:1}" == "f" ]; then
    echo "Fluidics feature containers are being prepared to run"
    for JOB_YAML in jobs/fluidics/*.yaml; do
     #   kubectl delete job ${JOB_YAML}
        echo "Running ${JOB_YAML}"
        envsubst < ${JOB_YAML} | kubectl create -f - 
    done
elif [ "${UUID:11:1}" == "i" ]; then
    echo "Imaging feature containers are being prepared to run"
    for JOB_YAML in jobs/imaging/*.yaml; do
     #   kubectl delete job ${JOB_YAML}
        echo "Running ${JOB_YAML}"
        envsubst < ${JOB_YAML} | kubectl create -f - 
    done
fi


