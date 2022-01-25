#!/usr/bin/env python
'''
Root to numpy converter (from file to file)

Read the most recent version of ROOT files with EMCal testbeam.

The first index in the array is the 64 channel numbers
and the second is the time steps of the waveform.
Branch name is 'electron_adc_counts'.

The 32nd time bin of the waveform always contains -999 and is useless,
so by default we exclude it
'''

##################################
import uproot
import numpy as np
import matplotlib.pyplot as plt
import argparse
##################################

#####################################

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--csvout",   type=str,
                    help="If specified, name of the CSV file to output the data sample to and exit", default='')

parser.add_argument("-i", "--infile",   type=str,   help="Input ROOT file",     default='')
parser.add_argument("-o", "--outfile",  type=str,   help="Output numpy file",   default='')

parser.add_argument("-N", "--entries",  type=int,   help="Number of samples",   default=0)
parser.add_argument("-L", "--bins",     type=int,   help="Number of bins",      default=31)

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-z", "--zip",      action='store_true',    help="Store compressed")

################################################################
args        = parser.parse_args()

infile      = args.infile
outfile     = args.outfile

entries     = args.entries
L           = args.bins

verbose     = args.verbose

if(infile==''):
    print('Please specify a valid ROOT filename (input)')
    exit(-1)

if(outfile==''):
    print('Please specify a valid numpy filename (output)')
    exit(-1)

file    = uproot.open(infile)
dir     = file['T;1']

Nentries = dir['electron_adc_counts'].num_entries

if entries==0:
    N = Nentries
else:
    N = min(entries,Nentries)

if verbose: print(f'''Will process {N} entries''')

branch = dir['electron_adc_counts']

X = branch.array(library='np', entry_stop=N)

if verbose : print(f'''Created an array: {X.shape}''')


if verbose : print(f'''Saving to file {outfile} ''')

with open(outfile, 'wb') as f:
    if(args.zip):
        np.savez_compressed(f, X=X)
    else:
        np.save(f, X)

f.close()

exit(0)
