#!/usr/bin/python

import uuid
import os
from os.path import expanduser
import sys
import re
import json
import time
from datetime import datetime
import datetime
import pytz #convert between timezones
from pytz import timezone

home = expanduser("~")
filepath = home + "/id.json" #id.json should be in homedirectory

# Ensure an id.json exists
if(os.path.isfile(filepath)):
    print("id.json already exists")
    exit() #done

fd = open(filepath, "w")

# Make GUID
guid = str(uuid.uuid4()) #generate guid

# Current time in UTC
now_utc = datetime.datetime.now(timezone('UTC'))
# Convert to US/Pacific time zone
now_pacific = now_utc.astimezone(timezone('US/Pacific'))
# Specify date formatting
fmt = "%H:%M:%S %d-%m-%Y %Z%z"
# Make date timestamp
localdate_string = now_pacific.strftime(fmt)


input = input("Enter Type (#): \n (1) master\n (2) organoid-simulated\n (3) organoid-real\n")



if (input == "1"):
    type = "master"
elif (input == "2"):
    type = "organoid-simulated"
elif (input == "3"):
    type = "organoid-real"


# Put JSON together
data = {
	"resource": {
		"guid": guid,
		"type": type,
		"date-online": localdate_string
    }
}

# Save JSON file
with open(filepath, 'w') as fp:
		json.dump(data, fp)

print("Saved!\n")

# Display JSON
print(json.dumps(data, indent=4))
