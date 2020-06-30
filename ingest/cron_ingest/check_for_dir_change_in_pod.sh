
#!/bin/bash

declare -a current_files_in_dir
declare -a last_time_files_in_dir


last_time_files_in_dir=()
while IFS= read -r line || [[ "$line" ]]; do
  last_time_files_in_dir+=("$line")
done < 'current_files_in_dir.txt'

current_files_in_dir=()
while IFS= read -r line || [[ "$line" ]]; do
  current_files_in_dir+=("$line")
done < 'files_in_dir.txt'


#echo ${last_time_files_in_dir[*]}
#echo ${current_files_in_dir[*]}

A=${current_files_in_dir[@]};
B=${last_time_files_in_dir[@]};
if [ "$A" == "$B" ] 
then
  echo "Are the same"
  touch "uuid.txt"
  export UUID="" 
else
  NEW_EXPERIMENTS_STRING=`echo ${current_files_in_dir[@]} ${last_time_files_in_dir[@]} | tr ' ' '\n' | sort | uniq -u`

  NEW_EXPERIMENTS_LIST=( $NEW_EXPERIMENTS_STRING )
  
  echo "This is NNEW_EXPERIMENT:"                                                                                                     
  echo ${NEW_EXPERIMENTS_STRING}   

  for NEW_EXPERIMENT in $NEW_EXPERIMENTS_STRING
  do
    echo $NEW_EXPERIMENT
  
    export UUID="${NEW_EXPERIMENT%.zip}"
 
    python3 download_from_prp.py

    python3 prp_ingest.py

    python3 upload_to_prp.py

    source run_jobs.sh

    echo "$UUID" > "uuid.txt"
  done
fi
