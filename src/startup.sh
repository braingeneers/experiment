#!/bin/sh

# Pull latest code from GitHub
cd ~/experiment
git pull


# Launch Organoid Program
filepath="$HOME/id.json" #stores program attribute


if grep -q -F "master" $filepath; then
  # Launch master program
  python3 /src/master.py
  echo "Master Launched: master.py"

if grep -q -F "organoid-simulation" $filepath; then
  #launch real organoid wrapper
  python3 /src/organoidWrapper.py
  echo "Simulation Wrapper Launched: organoidWrapper.py"

if grep -q -F "organoid-real" $filepath; then
  #launch simulation organoid wrapper
  make
  ./src/arrayWrapper
  echo "Organoid Wrapper Launched: arrayWrapper.py"

else
  echo "No indication of program type (master, organoid-simulation, organoid-simulation) in ~/id.json"

fi
