
#!/bin/bash

source pull_git_jobs.sh

python3 create_current_files_in_dir.py

declare -a current_files_in_dir

current_files_in_dir=()
while IFS= read -r line || [[ "$line" ]]; do
  current_files_in_dir+=("$line")
done < 'files_in_dir.txt'


echo ${current_files_in_dir[*]}

A=${current_files_in_dir[@]};

for NEW_EXPERIMENT in $(cat current_files_in_dir.txt )
do
  echo $NEW_EXPERIMENT
  
  export UUID="${NEW_EXPERIMENT%.zip}"
 
  python3 download_from_prp.py

  python3 prp_ingest.py

  python3 upload_to_prp.py

  source run_jobs.sh

done

