"""
Ingest White-Matter eCube to Braingeneers
"""
import os
import re
import struct
import datetime
import argparse
import numpy as np
import shutil


def datetime_to_ntp(ts):
    """
    Convert python datetime into an Internet Network Time
    Protocol (NTP) 64bit timestamp
    """
    diff = ts - datetime.datetime(1900, 1, 1, 0, 0, 0)
    return np.uint64((int(diff.total_seconds()) << 32)
                     + (diff.microseconds / 1000000 * 2**32))


parser = argparse.ArgumentParser(description="Ingest eCube to Braingeneers")
parser.add_argument('--output', required=True, help="Output directory")
parser.add_argument('files', nargs='*', help="Files to convert")
args = parser.parse_args()

for f in args.files:
    # Extract timestamp from filename as the one in the original file is wrong
    ds = datetime.datetime(*[
        int(c) for c in re.findall(r"(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)", f)[0]])

    # Copy over the original file
    shutil.copyfile(f, os.path.join(args.output, os.path.basename(f)))

    # Overwrite timestamp
    with open(os.path.join(args.output, os.path.basename(f)), "r+b") as fd:
        fd.write(struct.pack('Q', datetime_to_ntp(ds)))
