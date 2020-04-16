import braingeneers.datasets_electrophysiology                                                                                        
import os                                                                                                                             
import numpy as np
                                                                                                                                      UUID = str(os.getenv('UUID') )
                                                                                                                                      batch=braingeneers.datasets_electrophysiology.load_batch(UUID)
                                                                                                                                      os.mkdir('/public/groups/braingeneers/ephys/'+UUID+'/example_spikes')

for experiment in batch['experiments']:
    #example spike sorting algorithm runs                                                                                             
    with open('/public/groups/braingeneers/ephys/'+UUID+'/example_spikes/'+experiment[:-5]+'.npy', 'w') as fp:                        
        #example_spikes are put in the numpy file                                                                                     
        pass  
