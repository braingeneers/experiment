#!/bin/sh

job="@reboot $HOME/experiment/src/startup.sh &"
# If not present, add startup cron job on machine:
if ! crontab -l | grep -q -F job; then
    (crontab -l && echo job) | crontab -
    echo "Added cron job: "
    echo job
fi

#install requirements
#pip install ...


#reboot
reboot -f
