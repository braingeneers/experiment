
#!/bin/bash

# pulls the jobs for analysis that will be run after ingest

source pull_git_jobs.sh

python3 create_current_files_in_dir.py

declare -a current_files_in_dir

current_files_in_dir=()
while IFS= read -r line || [[ "$line" ]]; do
  current_files_in_dir+=("$line")
done < 'files_in_dir.txt'


echo ${current_files_in_dir[*]}

A=${current_files_in_dir[@]};


# the for loop goes through every zip file in s3://braingeneers-inbox/
#-------------------------------------------------------------
for NEW_EXPERIMENT in $(cat current_files_in_dir.txt )
do
  echo $NEW_EXPERIMENT
  
  export UUID="${NEW_EXPERIMENT%.zip}"
 
  python3 download_from_prp.py

  python3 prp_ingest.py
  
  # After the prp_ingest.py code runs there s3://braingeneers/ephys/0000-00-00-e-info/original/ and s3://braingeneers/ephys/0000-00-00-e-info/derived/ are created
  #-----------------------------------------------------------
  python3 upload_to_prp.py
  

  # jobs will get kicked off with source run_jobs.sh 
  #--------------------------------
  source run_jobs.sh

done

