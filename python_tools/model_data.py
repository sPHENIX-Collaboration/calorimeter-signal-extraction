#!/usr/bin/env python

'''
TF model creation based on test beam data and fitting
'''

import argparse
from typing import Optional

import numpy as np
from numpy import loadtxt

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.vis_utils import plot_model

from keras.regularizers import l1

################################
def yes_or_no(question):
    while "the answer is invalid":
        inp = input(question)
        reply = inp.lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

################################
parser = argparse.ArgumentParser()

# I/O options
parser.add_argument("-i", "--infile",   type=str,   help="Input file (numpy)", default='')
parser.add_argument("-s", "--savefile", type=str,   help="Filename to save the model", default='')
parser.add_argument("-p", "--plot",     type=str,   help="If specified, Name of the PNG file to plot the model to and exit", default='')


# ML options
parser.add_argument("-b", "--batch",    type=int,   help="Batch size",              default=10)
parser.add_argument("-e", "--epoch",    type=int,   help="Epoch",                   default=100)

parser.add_argument("-l", "--loss",     type=str,   help="Loss function", default='mse')
parser.add_argument("-a","--activation",type=str,   help="Last layer activation", default='linear')
parser.add_argument("-o", "--optimizer",type=str,   help="Optimizer", default='adam')

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")

args    = parser.parse_args()

infile  = args.infile
save    = args.savefile
plot    = args.plot

# Model Training
batch   = args.batch
epoch   = args.epoch
loss    = args.loss
act     = args.activation
opt     = args.optimizer

verbose = args.verbose

if infile == '':
    print('Please specify the input file name')
    exit(-1)

# Load the dataset
with open(infile, 'rb') as f: dataset = np.load(f)
if verbose: print(f'''Read an array: {dataset.shape}''')

L = len(dataset[0]) - 3 # three trailing numbers are "y"

# Split into input (X) and output (y) variables
X = dataset[:,0:L]
y = dataset[:,(L):(L+3)] # the "y" vector: origin, peak value, pedestal

# for i in range(0,4): print(X[i], '!', y[i])

# Define the Keras model
model = Sequential()
model.add(Dense(L, input_dim=L, activation='relu'))
model.add(Dense(3, activation=act))

if plot!='':
    plot_model(model,   to_file=plot,    show_shapes=True,  show_dtype=True,    show_layer_names=True,
    rankdir="TB",       expand_nested=True, dpi=96,  layer_range=None,)
    exit(0)

# Compile the Keras model
model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

# Fit the keras model on the dataset
model.fit(X, y, epochs=epoch, batch_size=batch) #, callbacks=[])

# Evaluate the accuracy of the model
_, accuracy = model.evaluate(X, y)
print('Accuracy: %.2f' % (accuracy*100))

if yes_or_no('Save model? (y/n) '):
    print('Save')
    if save=='': exit(0)
    model.save(save)
else:
    print('Bye')
    exit(0)

exit(0)

