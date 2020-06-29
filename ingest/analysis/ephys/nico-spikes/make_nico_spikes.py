print('Importing spikeinterface. It will take a little bit.')
import spikeinterface
import spikeinterface.extractors as se
import spikeinterface.toolkit as st
import spikeinterface.sorters as sorters
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw
import matplotlib.pylab as plt
import os
import braingeneers.datasets_electrophysiology
import numpy as np
import shutil
from numpy import genfromtxt

UUID=os.getenv('UUID')

#the directory for all the stuff we don't need but is made anyways
path_for_spike_stuff = str('/public/groups/braingeneers/ephys/'+UUID+'/other_spike_stuff')

if not os.path.exists(path_for_spike_stuff):
    os.mkdir(path_for_spike_stuff)

os.mkdir('/public/groups/braingeneers/ephys/' + UUID + '/nico_spikes/')

batch_metadata = braingeneers.datasets_electrophysiology.load_batch(UUID)

for i in range(len(batch_metadata['experiments'])):

    print('check')
    print(UUID,'Experiment:', i)

    blocks = np.transpose(braingeneers.datasets_electrophysiology.load_blocks(UUID, i)[0])

    print("Block shape", str(blocks.shape))                                                                         
                                                                                                                    
    geom = genfromtxt('256ANS_locs.csv', delimiter=',')                                                             

    geom = geom[1:129]                                                                                              
                                                                                                                    
    print('Geom Shape:  ' +str(geom.shape))                                                                         
                                                                                                                    
    experiment_metadata=braingeneers.datasets_electrophysiology.load_experiment(UUID, i)
                                                                                                                    
    fs =experiment_metadata["sample_rate"]                                                                          
                                                                                                                    
    recording=se.NumpyRecordingExtractor(
        timeseries=blocks,
        geom=geom,                                                                                                  
        sampling_frequency=fs                                                                                       
    )                                                                                                               

    channel_ids = recording.get_channel_ids()
                                                                                                                    
    fs = recording.get_sampling_frequency()
                                                                                                                    
    num_chan = recording.get_num_channels()                                                                         
                                                                                                                    
    recording_f = st.preprocessing.bandpass_filter(recording, freq_min=300, freq_max=6000)
    recording_cmr = st.preprocessing.common_reference(recording_f, reference='median')                              
                                                                                                                    
    sorting_MS4 = sorting_MS4 = sorters.run_mountainsort4(recording_f, num_workers=15,                              
                                    freq_min=None, freq_max=None, filter=False,
                                    detect_threshold=5, detect_interval= 20,                                        
                                   adjacency_radius=None)
                                   
    try:                           
        st.postprocessing.export_to_phy(recording_f, sorting_MS4, output_folder=path_for_spike_stuff)
    except (TypeError, ValueError):
            print('This is normal')

#         #Convert firings.mda to npy and move to the right place
        #----------------------------------------------------------------------------------------  
    import spikeextractors.extractors.mdaextractors.mdaio

    path_of_firings = 'tmp_mountainsort4/firings.mda'

    if os.path.isfile(path_of_firings):
        spikes = spikeextractors.extractors.mdaextractors.mdaio.readmda(path_of_firings)
    else:
        raise Exception('The path does not exist for the spikes')

    path_to_save_spike = '/public/groups/braingeneers/ephys/' + UUID + '/nico_spikes/' \
    + batch_metadata["experiments"][i][:-5].rsplit('/',1)[-1] + '_spikes.npy'

    print('Saving', path_to_save_spike)
    
    np.save(path_to_save_spike, spikes)

shutil.rmtree(path_for_spike_stuff)

    #the directory is not useful now that we have the spikes
shutil.rmtree('tmp_mountainsort4')

print('Finished Ingesting Batch')
