import os
import re
import sys
import glob
import json
import argparse
import datetime
import numpy as np

import read_data


parser = argparse.ArgumentParser(
    description="Ingest a batch of experiments")
parser.add_argument('--uuid', required=True,
                    help="UUID for batch")
parser.add_argument('--issue', required=True,
                    help="Github issue is in internal")
args = parser.parse_args()


# Batch = set of folders each with an experiment and all its recordings

print("Ingesting batch {}".format(args.uuid))

os.makedirs("derived/{}".format(args.uuid), exist_ok=True)

batch_metadata = {
    "uuid": args.uuid,
    "issue": "https://github.com/braingeneers/internal/issues/{}".format(args.issue),
    "notes": "\n".join([open(f).read() for f in glob.glob("original/{}/*.txt".format(args.uuid))])
}

experiments = []

# Add any metadata from json files to the batch metadata
for f in glob.glob("original/{}/*.json".format(args.uuid)):
    batch_metadata.update(json.load(open(f)))

# Ingest each experiment and exhaust in normalized form into derived/<args.uuid>/
for original_path in sorted(glob.glob("original/{}/*/".format(args.uuid))):

    experiment_metadata = {}

    experiment_metadata["name"] = os.path.basename(
        os.path.normpath(original_path)).replace(" ", "-")
    print("Experiment {} from {}".format(experiment_metadata["name"], original_path))

    # Concatenate all *.txt files into a "notes" field
    experiment_metadata["notes"] = "\n".join(
        [open(f).read() for f in glob.glob("{}/*.txt".format(original_path))])

    # Walk through each *.rhd in the experiment sorted alphabetically and therefore by time
    experiment_metadata["samples"] = []
    for sample_path in sorted(glob.glob("{}/*.rhd".format(original_path))):

        print("Sample {}".format(sample_path))

        # Try reading its *.rhd file stopping if there is an error. Any earlier
        # samples in the run will be retained and stored but with an "error" field
        # in the experiments metadata
        try:
            data = read_data.read_data(sample_path)
        except Exception as e:
            experiment_metadata["error"] = "{}: {}".format(sample_path, str(e))
            print("ERROR: {}".format(experiment_metadata["error"]))
            break

        sample_metadata = {}

        sample_metadata["num_samples"] = data["num_amplifier_samples"]

        sample_metadata["name"] = os.path.splitext(
            os.path.basename(sample_path).replace(" ", "-"))[0]

        sample_metadata["timestamp"] = datetime.datetime.strptime(
            re.findall(r"_(\d+_\d+)", sample_metadata["name"])[0], "%y%m%d_%H%M%S").isoformat()

        if "timestamp" not in batch_metadata:
            batch_metadata["timestamp"] = sample_metadata["timestamp"]

        # Add all the Intan metadata - < is a hack to exclude all sample data
        sample_metadata.update({k: v for k, v in data.items() if sys.getsizeof(v) < 2048})

        sample_metadata["original"] = sample_path
        sample_metadata["derived"] = "derived/{}/{}.npy".format(args.uuid, sample_metadata["name"])

        # Save the original un-modified np.uint16 to save space and so there is no loss of accuracy
        sample_metadata["units"] = "µV"
        sample_metadata["offset"] = 32768
        sample_metadata["scaler"] = 0.195
        np.save(sample_metadata["derived"], data["amplifier_data"])

        experiment_metadata["samples"].append(sample_metadata)

    # Add any metadata from json files to the experiment metadata
    for f in glob.glob("{}/*.json".format(original_path)):
        experiment_metadata.update(json.load(open(f)))

    # Save the meta data for this experiment
    with open("derived/{}/{}.json".format(args.uuid, experiment_metadata["name"]), "w") as f:
        json.dump(experiment_metadata, f, sort_keys=True)

    experiments.append({
        "path": "derived/{}/{}.json".format(args.uuid, experiment_metadata["name"]),
        "timestamp": experiment_metadata["samples"][0]["timestamp"]
    })

# Add paths in timestamp order
batch_metadata["experiments"] = [
    e["path"] for e in sorted(experiments, key=lambda k: k['timestamp'], reverse=False)]

with open("derived/{}/metadata.json".format(args.uuid), "w") as f:
    json.dump(batch_metadata, f, sort_keys=True)

print("Finished ingesting batch.")
