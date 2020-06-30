import os 
import glob
import argparse
import re
import datetime
import read_data
import sys
import numpy as np
import struct
import json
import shutil
import grab_files_from_derived
from numpy import genfromtxt
import pickle

#with open ('uuid.txt', 'rb') as fp: 
#    args_uuid = str(pickle.load(fp))

args_uuid = os.getenv('UUID')

#args_uuid = '0000-00-00-e-stuff'
args_issue = '0'
# #Creates the arguments of uuid and issue
# #--------------------------------------------------------------------------------
# parser = argparse.ArgumentParser(
#     description="Ingest a batch of experiments")
# parser.add_argument('--uuid', required=True,
#                     help="UUID for batch")
# parser.add_argument('--issue', required=True,
#                    help="Github issue is in internal")
# args = parser.parse_args()
# #--------------------------------------------------------------------------------



#Checking if the uuid is correct
#--------------------------------------------------------------------------------
if len(args_uuid) < 11:
    raise Exception('The uuid is too short. Make sure you are using the right format.')
     
if args_uuid[11] == 'i' or args_uuid[11] == 'e'or args_uuid[11] == 'f':
    print('The formatting for group specification is correct.')
else:
    raise Exception('Make sure you created the uuid in the correct format because \
                    the identification of the experiment is not in the 12th character place on the uuid.')
#--------------------------------------------------------------------------------

#Check for Imaging 
#--------------------------------------------------------------------------------
if args_uuid[11] == 'i':
    print('The ingest for imaging is starting.')
    if os.path.isdir('/public/groups/braingeneers/Imaging/'+ args_uuid  + '/derived/'):
        raise FileExistsError('Some body has already ingested this batch. \n If you want to ingest it again you will have to run: \
                              rm -r /public/groups/braingeneers/Imaging/'+args_uuid+'/derived/  to delete the past ingest. \
                              \n BE CAREFUL!!!!!!!!')
        
        
    shutil.copytree('/public/groups/braingeneers/Imaging/' + args_uuid + '/original/' , 'Imaging/' + args_uuid + 'derived/')
    print('The images in original have been copied to derived')
#--------------------------------------------------------------------------------

#Check for Fluidics
#--------------------------------------------------------------------------------
elif args_uuid[11] == 'f':
    print('There is no ingest for fluidics data. It is already ready to read.') 
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
elif args_uuid[11] == 'e':
    
   
    print('The ingest for electrophysiology is starting.')
    print("/public/groups/braingeneers/ephys/{}/original/*.rhs".format(args_uuid))
    if len(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhs".format(args_uuid)))==0 \
    and len(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid))) ==0:
        print("There are no rhd or rhs files. Must not be from UCSC")\
        
    elif len(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhs".format(args_uuid)))>0 \
    or len(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid))) >0:
        
        print("There are rhs or rhd files")
        
    #Converts datetime to ntp
    #----------------------------------------------------------------------------------------
    def datetime_to_ntp(ts):
        diff = ts - datetime.datetime(1900, 1, 1, 0, 0, 0)
        return np.uint64((int(diff.total_seconds()) << 32) + (diff.microseconds / 1000000 * 2**32))
    #---------------------------------------------------------------------------------------------------
    
    if os.path.isdir("/public/groups/braingeneers/ephys/{}/derived/".format(args_uuid)):
            raise FileExistsError('Some body has already ingested this batch. \n If you want to ingest it again \
                                  you will have to run: \
                                  rm -r /public/groups/braingeneers/ephys/'+args_uuid+'/derived/  \
                                  to delete the  past ingest. \n BE CAREFUL!!!!!!!!')
    os.makedirs("/public/groups/braingeneers/ephys/{}/derived/".format(args_uuid, exist_ok=True))
    #declares batch_metadata
    batch_metadata = {
    "uuid": args_uuid,
    "issue": "https://github.com/braingeneers/internal/issues/{}".format(args_issue),
    "notes": open("/public/groups/braingeneers/ephys/{}/original/batch.txt".format(args_uuid)).read() \
        if os.path.exists("/public/groups/braingeneers/ephys/{}/original/batch.txt".format(args_uuid)) else "",
    "notes": open("/public/groups/braingeneers/ephys/{}/original/batch.txt".format(args_uuid)).read() \
        if os.path.exists("/public/groups/braingeneers/ephys/{}/original/batch.txt".format(args_uuid)) else "",
    "email": open("/public/groups/braingeneers/ephys/{}/original/email.txt".format(args_uuid)).read() if os.path.exists("/public/groups/braingeneers/ephys/{}/original/email.txt".format(args_uuid)) else ""}
    
    experiments = []

    rhss = sorted(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhs".format(args_uuid, exist_ok=True)))
    experiment_names_rhs = sorted(set(
        [re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhs", s)[0][2].split('/')[-1] for s in rhss]))

    rhds = sorted(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid, exist_ok=True)))
    experiment_names_rhd = sorted(set(
        [re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhd", s)[0][2].split('/')[-1] for s in rhds]))

    print("These are the experiment names of rhs ", (experiment_names_rhs))
    print("These are the experiment names of rhd ", (experiment_names_rhd))

    if len(experiment_names_rhd) == 0:
        experiment_names = experiment_names_rhs

    elif len(experiment_names_rhs) == 0:
        experiment_names = experiment_names_rhd

    else:
        experiment_names_rhs.extend(experiment_names_rhd)
        experiment_names = experiment_names_rhs

    #----------------------------------------------------------------------------------------
    
    #Setting Experiment Metadata
    #--------------------------------------------------------------------------------------------
    for experiment_name in experiment_names:
        print("Ingesting experiment", experiment_name)

        experiment_metadata = {}

        experiment_metadata["name"] = experiment_name

        print('--------------experiment_name:  '+experiment_name)

        experiment_metadata["offset"] = 0               

        experiment_metadata["units"] = "\u00b5V"

        experiment_metadata["scaler"] = 0.195

        experiment_metadata["version"]="0.0.1"

        experiment_metadata["blocks"]=[]         
    #---------------------------------------------------------
    
    # Add <experiment_name>.txt to the notes field
    #---------------------------------------------------------
    
        print('Path for notes :', "/public/groups/braingeneers/ephys/{}/original/{}.txt".format(args_uuid, experiment_name))
        if os.path.exists("/public/groups/braingeneers/ephys/{}/original/{}.txt".format(args_uuid, experiment_name)):
            experiment_metadata["notes"] = open(
                "/public/groups/braingeneers/ephys/{}/original/{}.txt".format(args_uuid, experiment_name)).read()
        else:
            experiment_metadata["notes"] = ""
    #-----------------------------------------------------------------------------
    
    # Find all the rhd's and rhs's that match the experiment name and walk through in sorted/time order
    #------------------------------------------------------------------------------------------------
        experiment_metadata["channels"] = []
        print("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid, exist_ok=True))
        for p in sorted(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid))):
            print('This is p', p)
            
        rhds = [p for p in sorted(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhd".format(args_uuid, exist_ok=True)))
                if re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhd", p)[0][2].split('/')[-1] == experiment_name]
        print("Original rhd files to ingest:", rhds)

        rhss = [p for p in sorted(glob.glob("/public/groups/braingeneers/ephys/{}/original/*.rhs".format(args_uuid, exist_ok=True)))
                if re.findall(r"(.*?)\/(.*?)\/(.*?)_(\d{6}_\d{6}).rhs", p)[0][2].split('/')[-1] == experiment_name]
        print("Original rhs files to ingest:", rhss)

        if len(rhds) > 0:
            timestamp_for_experiment_metadata= os.path.splitext(
                    os.path.basename(rhds[0]).replace(" ", "-"))[0]

        if len(rhss) > 0:
            timestamp_for_experiment_metadata= os.path.splitext(
                    os.path.basename(rhss[0]).replace(" ", "-"))[0]



        experiment_metadata["timestamp"] = datetime.datetime.strptime(
                re.findall(r"_(\d{6}_\d{6})", timestamp_for_experiment_metadata)[0], "%y%m%d_%H%M%S").isoformat()
    #-------------------------------------------------------------------------------------------
    
    # Try reading its rhs or rhd files 
    #-------------------------------------------------------------------------------------------
        if len(rhss) > 0:
            files_to_ingest = rhss
        elif len(rhds)> 0:
            files_to_ingest = rhds       


        for sample_path in files_to_ingest:
            print("Reading sample {}".format(sample_path))

            if len(rhss) > 0:
                data = load_intan_rhs_format.read_data(sample_path)
                #np.save("stim_data.npy", data['stim_data'])


            elif len(rhds)> 0:
                data = read_data.read_data(sample_path)
                print('------------------', type(data))

           # print("-------data[stim_parameters].keys", data['stim_parameters'].keys())

           # for i in data['stim_parameters']:
            #    print(i, data['stim_parameters'][i])

            get_samples={} 

            get_samples.update({k: v for k, v in data.items() if sys.getsizeof(v) < 2048})




            experiment_metadata["sample_rate"]= int(get_samples["frequency_parameters"]["amplifier_sample_rate"])


    #-------------------------------------------------------------------------------------------
    
    #Setting metadata
    #-------------------------------------------------------------------------------------------           
            sample_metadata = {}

            print("This is the sample path", sample_path)

            sample_metadata["num_samples"] = data["num_amplifier_samples"]

            sample_metadata["name"] = os.path.splitext(
                os.path.basename(sample_path).replace(" ", "-"))[0]

            block_timestamp = datetime.datetime.strptime(
                re.findall(r"_(\d{6}_\d{6})", sample_metadata["name"])[0], "%y%m%d_%H%M%S")

            check_this=0

            check_this=check_this+1

            if check_this==1:
                write_timestamp=block_timestamp

            experiment_metadata['blocks'].append({'timestamp': str(block_timestamp.isoformat()),
                                                  'path': '{}bin'.format(str(sample_path).split("/")[-1][:-3]),
                                                  'source': sample_path, 
                                                  'num_frames':data["amplifier_data"].shape[1]}) 

            if "timestamp" not in batch_metadata:

                print("This is the type of experiment_metadata[timestamp]", experiment_metadata["timestamp"])

                batch_metadata["timestamp"] = experiment_metadata["timestamp"]

            sample_metadata["original"] = sample_path

            sample_metadata["derived"] = "ephys/derived/{}/{}.npy".format(args_uuid, sample_metadata["name"])

            print("---------------------get samples.keys()", get_samples.keys())


#            experiment_metadata["channels"] = (get_samples["amplifier_channels"])

           # for i in range(32):

            #    experiment_metadata["channels"].append([])

            if len(rhss)>0:

                experiment_metadata["num_channels"] = int(data['amplifier_data'].shape[0])*2

                experiment_metadata["num_current_input_channels"] = int(data['amplifier_data'].shape[0])

            elif len(rhds)>0:

                experiment_metadata["num_channels"] = int(data['amplifier_data'].shape[0])

                experiment_metadata["num_current_input_channels"] = 0

            experiments.append({
            "path": "{}.json".format(experiment_metadata["name"]),
            "timestamp": experiment_metadata["timestamp"]
    })

            experiment_metadata['num_voltage_channels'] = int(data['amplifier_data'].shape[0])

            if len(rhss) > 0:

                print("------------------this is the shape of stim data", data['stim_data'].shape)

                print("------------------this is the shape of actual data", data['amplifier_data'].shape)

                #experiment_metadata['num_channels'] = int(data['stim_data].shape[0])+ int(data['amplifier_data].shape[0])



                subtracted_data = data['amplifier_data']-32768

                print("First frame:", subtracted_data[:,0]*.195)

                print("Second frame:", subtracted_data[:,1]*.195)

                stim_data_reformatted = (data['stim_data']/(.195)) 

                #put_this_in_binary = np.concatenate((subtracted_data, stim_data_reformatted), axis = 0)

                i=0
                put_this_in_binary =[]
                while( i< (subtracted_data.shape[1])):
                    put_this_in_binary.extend(subtracted_data[:,i])
                    put_this_in_binary.extend(stim_data_reformatted[:,i])
                    i= i+1

                put_this_in_binary = np.array(put_this_in_binary)

                print("------------------this is the shape of full data", len(put_this_in_binary))

               # print("------------------this is the first channel", put_this_in_binary[0]*.195)

            elif len(rhds) > 0:

                put_this_in_binary = data['amplifier_data']

                put_this_in_binary = put_this_in_binary.astype(np.int32)-32768      

            with open("/public/groups/braingeneers/ephys/{}/derived/{}.bin".format(args_uuid, sample_metadata["name"]), "wb") as f:
                print("Writing the timestamp in the bin file")

                f.write(struct.pack('Q', datetime_to_ntp(write_timestamp)))

                print("Writing the numpy array in the bin file")

                put_this_in_binary.astype('int16').tofile(f)   

    #-------------------------------------------------------------------------------------------
    
    #Save the meta data for this experiment
    #-------------------------------------------------------------------------------------------

        with open("/public/groups/braingeneers/ephys/{}/derived/{}.json".format(args_uuid, experiment_metadata["name"]), "w") as f:

            json.dump(experiment_metadata, f, sort_keys=True)
    #------------------------------------------------------------------------------------------
    # Add paths in timestamp order and save data
    #--------------------------------------------------------------------------------------
    batch_metadata["experiments"] = [
        e["path"] for e in sorted(experiments, key=lambda k: k['timestamp'], reverse=False)]

    batch_metadata["experiments"] = list(set(batch_metadata['experiments']))
    with open("/public/groups/braingeneers/ephys/{}/derived/metadata.json".format(args_uuid, exist_ok=True), "w") as f:

        json.dump(batch_metadata, f, sort_keys=True)
    #------------------------------------------------------------------------------------------
    
#Nico's spike sorting!!!!!!
# # ------------------------------------------------------------------------

#     print('Importing spikeinterface. It will take a little bit.')
#     import spikeinterface
#     import spikeinterface.extractors as se 
#     import spikeinterface.toolkit as st
#     import spikeinterface.sorters as sorters
#     import spikeinterface.comparison as sc
#     import spikeinterface.widgets as sw
#     import matplotlib.pylab as plt
    
#     #the directory for all the stuff we don't need but is made anyways
#     path_for_spike_stuff = str('/public/groups/braingeneers/ephys/'+args_uuid+'/other_spike_stuff')

#     if not os.path.exists(path_for_spike_stuff):
#         os.mkdir(path_for_spike_stuff)
        
#     path_for_actual_spikes = str('/public/groups/braingeneers/ephys/'+args_uuid+'/nico_spikes')

#     if not os.path.exists(path_for_actual_spikes):
#         os.mkdir(path_for_actual_spikes)
    
#     for i in range(len(batch_metadata['experiments'])):
        
#         print('check')
#         print(args_uuid, i)
#         test_blocks = grab_files_from_derived.load_blocks(args_uuid, i)
        
#         blocks = np.transpose(grab_files_from_derived.load_blocks(args_uuid, i)[0])
        
#         print('[[[[[[[[[[[[[[[[[[[[[[[   ' + str(blocks.shape))

#         geom = genfromtxt('256ANS_locs.csv', delimiter=',')

#         geom = geom[1:129]

#         print('Geom Shape:  ' +str(geom.shape))

#         fs =experiment_metadata["sample_rate"]

#         recording=se.NumpyRecordingExtractor(
#             timeseries=blocks,
#             geom=geom,
#             sampling_frequency=fs
#         )
        
#         channel_ids = recording.get_channel_ids()

#         fs = recording.get_sampling_frequency()

#         num_chan = recording.get_num_channels()

#         recording_f = st.preprocessing.bandpass_filter(recording, freq_min=300, freq_max=6000)
#         #recording_rm_noise = st.preprocessing.remove_bad_channels(recording_f, bad_channel_ids=[5])
#         recording_cmr = st.preprocessing.common_reference(recording_f, reference='median')

#         sorting_MS4 = sorting_MS4 = sorters.run_mountainsort4(recording_f, num_workers=15,
#                                         freq_min=None, freq_max=None, filter=True,
#                                         detect_threshold=5, detect_interval= 20,
#                                        adjacency_radius=None)

#         try:
#             st.postprocessing.export_to_phy(recording_f, sorting_MS4, output_folder=path_for_spike_stuff)
#         except (TypeError, ValueError):
#             print('This is normal')
        
# #         #Convert firings.mda to npy and move to the right place
#         #----------------------------------------------------------------------------------------  
#         import spikeextractors.extractors.mdaextractors.mdaio

#         path_of_firings = 'tmp_mountainsort4/firings.mda'

#         if os.path.isfile(path_of_firings):
#             spikes = spikeextractors.extractors.mdaextractors.mdaio.readmda(path_of_firings)
#         else:
#             raise Exception('The path does not exist for the spikes')
        
#     #    where_the_spike_is = '/public/groups/braingeneers/ephys/'+args_uuid+'/other_spike_stuff/spike_times.npy'
        

#         path_to_save_spike = '/public/groups/braingeneers/ephys/' + args_uuid + '/nico_spikes/' \
#         + batch_metadata["experiments"][i][:-5].rsplit('/',1)[-1] + '_spikes.npy'
        
#         print('Saving', path_to_save_spike)
        
#         np.save(path_to_save_spike, spikes)
        
#         #shutil.move(where_the_spike_is, path_to_save_spike)
#         #----------------------------------------------------------------------------------------  
        
    #the directory that contains all the files that we do not need is deleted.
#     shutil.rmtree(path_for_spike_stuff)
    
#     #the directory is not useful now that we have the spikes
#     shutil.rmtree('tmp_mountainsort4')
    
    print('Finished Ingesting Batch')
    
    

