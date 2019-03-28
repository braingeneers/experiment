#!/bin/sh

echo "Running setup.sh"

job="@reboot $HOME/experiment/src/startup.sh &"
# If not present, add startup cron job on machine:
if ! (crontab -l | grep -q -F "$job"); then
    (crontab -l ; echo "$job") | crontab -
    echo "Added cron job: "
    echo $job

fi


#install requirements
#pip install ...

# Ensure valid GUID exists
python3 guid.py


#reboot
reboot -f
