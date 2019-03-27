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
python3 organoidWrapper.py
