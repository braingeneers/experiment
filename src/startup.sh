#!/bin/sh

# Add as cron job  on machine:
# cron -e
# @reboot $HOME/experiment/src/startup.sh &

# Pull latest code from GitHub
cd ~/experiment/src
git pull

# Ensure valid GUID exists
python3 guid.py

# Launch main program
python3 arrayWrapper.py
#if grep -q -F "Master" "$HOME/guid.txt"; then
    # Launch Master
#    python3 master.py
#fi


# Launch Organoid Program
#if grep -q -F "Virtual" "$HOME/guid.txt"; then
  #launch organoid simulation wrapper
#  python3 organoidWrapper.py
#elif grep -q -F "Real" "$HOME/guid.txt";
  #Real
  #launch real organoid wrapper
#  python3 arrayWrapper.py
#fi
