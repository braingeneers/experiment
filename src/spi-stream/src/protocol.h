//-----------------------------------------------------------------------------
// Kateryna Voitiuk (kvoitiuk@ucsc.edu)
// Braingeneers
// protocol.h
// Description: Header file for master spi controller
//-----------------------------------------------------------------------------


#ifndef _MASTER_H
#define _MASTER_H

#include <bcm2835.h>
#include <stdio.h>

//P1-19 (MOSI)
//P1_21 (MISO)
//P1-23 (CLK)
//P1-24 (CE0)
//P1-26 (CE1)

//don't expext speed faster than 31MHz to work reliably on RasPi


/*
Metadata Output:
{
  "name": "name from experiment, usually set in Intan, or can be GUID",
  "notes": "Free form notes, any start of line times are relative to start",
  "timestamp": "UTC Start of experiment - may be before first block",
  "sample_rate": "",
  "offset": 32768,
  "scaler": 0.195,
  "units": "\u00b5V",
  "channels": [{
    "electrode_impedance_magnitude": 0.0,
    "electrode_impedance_phase": 0.0,
    "other parameters that can be extracted...",
  }],
  "blocks": [{
    "timestamp": "UTC timestamp for this block, allows for gaps in recording...",
    "num_samples": "Count of samples, here so we don't need to load in order to calculate",
    "path": "path to derived file ie npy or tfrecord under the braingeneers archive",
    "source": "optional path to original file, missing for simulated...",
  }],
}
*/



#endif  /*_MASTER_H*/
