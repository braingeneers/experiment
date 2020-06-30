import os
import json
import numpy as np

def load_batch(batch_uuid):
    print('In batch')

    full_path = '/public/groups/braingeneers/ephys/'+batch_uuid+'/derived/metadata.json'
    print('Full path in load_batch: ', full_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
           #print(json.load(f))
            return json.load(f)
    else: 
        raise Exception('The path did not exist for the json file.')
        
def load_experiment(batch_uuid, experiment_num):
  
    batch = load_batch(batch_uuid)
    print('after batch')
    print('batch["experiments"][experiment_num]', batch["experiments"][experiment_num])
    full_path = "/public/groups/braingeneers/ephys/"+batch_uuid+'/derived/' + batch["experiments"][experiment_num]
    print("Full Path: ", full_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            return json.load(f)

def load_blocks(batch_uuid, experiment_num, start=0, stop=None):
    
    print('check')
    metadata = load_experiment(batch_uuid, experiment_num)
    assert start >= 0 and start < len(metadata["blocks"])
    assert not stop or stop >= 0 and stop <= len(metadata["blocks"])
    assert not stop or stop > start

    def _load_path(path):
        with open(path, "rb") as f:
            f.seek(8, os.SEEK_SET)
            return np.fromfile(f, dtype=np.int16)

    def _load_url(url):
        with np.DataSource(None).open(url, "rb") as f:
            f.seek(8, os.SEEK_SET)
            return np.fromfile(f, dtype=np.int16)

    # Load all the raw files into a single matrix
    if os.path.exists("/public/groups/braingeneers/ephys/" + batch_uuid+ '/derived/'):
        # Load from local archive
        raw = np.concatenate([
            _load_path("/public/groups/braingeneers/ephys/{}/derived/{}".format(batch_uuid, s["path"]))
            for s in metadata["blocks"][start:stop]], axis=0)
    
    else:
        raise Exception('The file did not exist.')
    
    
    # Reshape interpreting as row major
    X = raw.reshape((-1, metadata["num_channels"]), order="C")
    # Convert from the raw uint16 into float "units" via "offset" and "scaler"
    X = np.multiply(metadata["scaler"], (X.astype(np.float32) - metadata["offset"]))

    # Extract sample rate for first channel and construct a time axis in ms
    fs = metadata["sample_rate"]

    start_t = (1000 / fs) * sum([s["num_frames"] for s in metadata["blocks"][0:start]])
    end_t = (1000 / fs) * sum([s["num_frames"] for s in metadata["blocks"][0:stop]])
    t = np.linspace(start_t, end_t, X.shape[0], endpoint=False)
    assert t.shape[0] == X.shape[0]

    return X, t, fs

        