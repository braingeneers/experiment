#!/usr/bin/python

import uuid
import os
import sys
import re

filepath = "../../guid.txt" #guid.txt should be outside of repository

#check if there exists a guid.txt with a valid GUID
fd = open(filepath, "r+")
contents = fd.read()
c = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', re.I)
result = c.match(contents)

if (result):
    exit() #done
else:
    #generate and write GUID to file
    guid = str(uuid.uuid4()) #generate guid
    fd.seek(0,0)
    fd.write(guid.rstrip('\r\n') + '\n' + contents)
