#!/bin/sh

# Pull latest code from GitHub
cd ~/experiment/src
git pull


# Launch Organoid Program
filepath="$HOME/id.json" #stores program attribute


if grep -q -F "master" $filepath; then
  # Launch master program
  python3 master.py
  echo "Master Launched: master.py"

elif grep -q -F "organoid-simulation" $filepath; then
  #launch real organoid wrapper
  python3 organoidWrapper.py
  echo "Simulation Wrapper Launched: organoidWrapper.py"

elif grep -q -F "organoid-real" $filepath; then
  #launch simulation organoid wrapper
  python3 arrayWrapper.py
  echo "Organoid Wrapper Launched: arrayWrapper.py"

else
  echo "No indication of program type (master, organoid-simulation, organoid-simulation) in ~/id.json"

fi
