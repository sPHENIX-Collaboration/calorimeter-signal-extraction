#!/usr/bin/env python
'''
Prepare a sample of the EMCAL test data previously saved as numpy files,
for ML training

This version adapted to the new data format:

The first index in the array is the 64 channel numbers
and the second is the time steps of the waveform.
Branch name is 'electron_adc_counts'.

The 32nd time bin of the waveform always contains -999 and is useless,
so by default we exclude it. That's why we use "L-1" in the code.
'''

##################################
from curses.ascii import LF
from os import ST_RDONLY

import  numpy as np
import  scipy
from    scipy.optimize import curve_fit

import  matplotlib.pyplot as plt
from    matplotlib import colors

import  argparse
import  platform
import  time
##################################

import  warnings
from    scipy.optimize import OptimizeWarning

##################################
# Local packages:
from fits import funcz
from fits.funcz import *

from utils.progress import *

##################################
peak_left, peak_right = (7,20) # will be cleaned up, temp solution
##################################

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--infile",   type=str,   help="Input numpy file",    default='')
parser.add_argument("-o", "--outfile",  type=str,   help="Output numpy file",   default='')

parser.add_argument("-l", "--left",     type=int,   help="Left limit",          default=0)
parser.add_argument("-r", "--right",    type=int,   help="Right limit",         default=31)

parser.add_argument("-L", "--bins",     type=int,   help="Number of bins",      default=31)
parser.add_argument("-N", "--Nevents",  type=int,   help="Number of events (zero for all)", default=0)
parser.add_argument("-n", "--nplot",    type=int,   help="Number of events to plot", default=10)

parser.add_argument("-t", "--threshold",type=int,   help="Signal threshold", default=300)

parser.add_argument("-c", "--channel",  type=int,   help="Channel",           default=-1)

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
################################################################
args        = parser.parse_args()

infile      = args.infile
outfile     = args.outfile

L           = args.bins
N           = args.Nevents

threshold   = args.threshold

nplot       = args.nplot
channel     = args.channel
verbose     = args.verbose
################################################################

python_info = platform.python_version_tuple()

if(verbose): print(f'''Python {python_info[0]}.{python_info[1]}.{python_info[2]}''')

if(infile==''):
    print('Please specify a valid input filename (input)')
    exit(-1)

with open(infile, 'rb') as f: X = np.load(f)
if verbose: print(f'''Completed reading an array: {X.shape}''')

data_length = X.shape[0]
if N<=0 or N>data_length: N = data_length # how many events to process

if verbose: print(f'''Will process {N} events''')

x   = np.linspace(0, 31, num=31, endpoint=False)
x1  = np.linspace(args.left, args.right, num=200, endpoint=False)
x2  = np.linspace(args.left, args.right, num=100, endpoint=False)

plt.style.use('seaborn-whitegrid')

new_length = L-1+5 # reserve 5 words for the training parameters

if (channel!=-1): 
    cnt_ped, cnt_sig, cnt_bad = (0, 0, 0)
    minima, x_min, x_max  = ([], [], [])
    r2s, amp, newamp, ampdiff, times, fxamp, fxt, newsaved = ([], [], [], [], [], [], [], [])

    dpd = []

    fig, ((ax1, ax2, ax3, nx1), (ax4, ax5, ax6, axx)) = plt.subplots(2,4)
    fig.set_size_inches(24.0, 12.0)
    fig.suptitle(f'''Channel {channel} pedestal and signal''')

    first           = True
    output_array    = None
    RuntimeError_cnt, RuntimeWarning_cnt, FloatingPointError_cnt, OptimizeWarning_cnt = (0, 0, 0, 0)

    ##################  IMPORTANT! ################
    np.seterr(over='raise')
    warnings.simplefilter("error", OptimizeWarning)

    ################# MAIN ########################

    land    = Landau()
    lfpd    = LandauFixedPed(0.0)

    if verbose: printProgressBar(0, N, prefix = 'Progress:', suffix = 'Complete', length = 100)

    for i in range(N): # loop over the data sample

        if verbose: printProgressBar(i + 1, N, prefix = 'Progress:', suffix = 'Complete', length = 100)

        frame = X[i]
        wave = frame[channel][0:31]
      
        lead = wave[0:5]
        pedestal = np.average(lead) # print(wave) print(pedestal)
        std      = np.std(lead)
        diff     = np.amax(lead) - np.amin(lead)

        maxdiff  = np.amax(diff)

        if(maxdiff<20 and std<7):
            minima.append(pedestal)
            x_min.append(i)

        maxindex    =   np.argmax(wave)
        maxval      =   wave[maxindex]

        if(maxval-pedestal)<threshold: continue # skip events below trigger
        
        if maxindex<peak_left or maxindex>peak_right:
            # if verbose: print('Outlier: ', maxindex, wave[maxindex])
            continue

        x_max.append(i)
    
        guess = [float(maxindex), float(2*(maxval-pedestal)), 1.0, float(pedestal), 1.0]

        Func    = land.fit

        try:
            popt, pconv = scipy.optimize.curve_fit(Func, x, wave, p0=guess)
        except RuntimeError:
            RuntimeError_cnt+=1
            continue
        except RuntimeWarning:
            RuntimeWarning_cnt+=1
        except FloatingPointError:
            FloatingPointError_cnt+=1
            continue
        except OptimizeWarning:
            OptimizeWarning_cnt+=1
            continue

        newamplitude    = land.peak(*popt) - pedestal
        amplitude       = maxval-pedestal
        calculated_r2   = funcz.r2(landau, vec=x, data=wave, pars=popt)

        r2s.append(calculated_r2)
        amp.append(amplitude)
        newamp.append(newamplitude)
        ampdiff.append(newamplitude-amplitude)
        dpd.append(popt[3]-pedestal)

        lfpd.pedestal = pedestal #    = LandauFixedPed(pedestal)
        Func    = lfpd.fit
        fixed_guess = np.take(popt, [0, 1, 2, 4])

        numbers = np.array(wave)
        n = 5
        indices = (-numbers).argsort()[:n]
        indices.sort()
        # for ind in indices: print(ind, numbers[ind])

        short_wave = np.take(wave, indices)

        try:
            popt_fx, pconv = scipy.optimize.curve_fit(Func, indices, short_wave, p0=fixed_guess)
        except RuntimeError:
            RuntimeError_cnt+=1
            continue
        except RuntimeWarning:
            RuntimeWarning_cnt+=1
        except FloatingPointError:
            FloatingPointError_cnt+=1
            continue
        except OptimizeWarning:
            OptimizeWarning_cnt+=1
            continue
        
        if(popt_fx[3]<0.0001): continue


        try:
            fxval = lfpd.peak(*popt_fx) - pedestal
        except FloatingPointError:
            FloatingPointError_cnt+=1
            continue

        times.append(land.origin(*popt))
        fxamp.append(fxval)
        fxt.append(lfpd.origin(*popt_fx))
        newsaved.append(newamplitude)

        if(cnt_sig<nplot):
            # print(short_wave)
            ax1.plot(x, wave, 'o') # , linestyle='solid', linewidth=1.5,)   # if(verbose): print(wave)
            cnt_sig+=1
            ax1.plot(x1, landau(x1, *popt))
            ax1.plot(x2, lfpd.fit(x2, *popt_fx), '+--')

            # if verbose: print('r2: ', calculated_r2)

        ################################## FINALIZE ########################
        peak    = land.peak(*popt)

        # adding the "Y" vector: origin, peak value, pedestal

        # --- FIXME --- origin is displaced
        result  = np.array([popt[0], peak, popt[3]])
        
        appended = np.append(wave, result)

        if first:
            output_array = np.array([appended])
            first = False
        else:
            output_array = np.append(output_array,[appended], axis=0)

    if verbose: print(f'''Created an array: {output_array.shape}''')

    if(outfile!=''):
        with open(outfile, 'wb') as f_out:
            np.save(f_out, output_array)

        f_out.close()

    if verbose:
        print(f'''
    RuntimeError {RuntimeError_cnt}
    RuntimeWarning {RuntimeWarning_cnt}
    FloatingPointError {FloatingPointError_cnt}
    OptimizeWarning {OptimizeWarning_cnt}
    ''')
    # Finalize the first graphic
    ax1.set_title(f'''A sample of waveforms (threshold={threshold})''')
    ax1.set_xlabel('Time bin')
    ax1.set_ylabel('ADC ch.')

    _ = ax2.hist2d(r2s, newamp, range=((0.4, 1.0), (-0.5, 4999.5)), bins=(100,50), norm=colors.LogNorm(1.0), cmap='plasma')
    ax2.set_title('R2 vs fit peak (Zlog)')
    ax2.set_xlabel('R2')
    ax2.set_ylabel('ADC ch.')


    _ = ax3.hist2d(r2s, newamp, range=((0.4, 1.0), (-0.5, 49.5)), bins=(100,50), norm=colors.LogNorm(1.0), cmap='plasma')
    ax3.set_title('ZOOM: R2 vs fit peak (Zlog)')
    ax3.set_xlabel('R2')
    ax3.set_ylabel('ADC ch.')

    _ = ax4.hist2d(dpd, newamp, range=((-0.5, 99.5), (-0.5, 4999.5)), bins=(100,50), norm=colors.LogNorm(1.0), cmap='plasma')
    ax4.set_title('Fit pedestal deviation vs Fit Peak (Zlog)')
    ax4.set_xlabel('Pedestal fit minus Leading bins avg')
    ax4.set_ylabel('ADC ch.')

    _ = ax5.hist2d(amp, newamp, range=((-0.5, 4999.5), (-0.5, 4999.5)), bins=(100,100), norm=colors.LogNorm(1.0), cmap='PuRd')
    ax5.set_title('Fit peak vs max channel (Zlog)')
    ax5.set_xlabel('Max Count - Ped')
    ax5.set_ylabel('Fit height')

    _ = ax6.hist2d(amp, newamp, range=((-0.5, 99.5), (-0.5, 99.5)), bins=(100,100), norm=colors.LogNorm(1.0), cmap='PuRd')
    ax6.set_title('ZOOM: Fit peak vs max channel (Zlog)')
    ax6.set_xlabel('Max Count - Ped')
    ax6.set_ylabel('Fit peak')

    _ = nx1.hist2d(times, fxt, range=((-0.5, 29.5), (-0.5, 29.5)), bins=(30,30), norm=colors.LogNorm(1.0), cmap='PuRd')
    nx1.set_title('Time: Quick vs Full fit (Zlog)')
    nx1.set_xlabel('Full')
    nx1.set_ylabel('Quick')

    _ = axx.hist2d(newsaved, fxamp, range=((0, 100), (0, 100)), bins=(100,100), norm=colors.LogNorm(1.0), cmap='PuRd')
    axx.set_title('Peak: Quick vs Full fit (Zlog)')
    axx.set_xlabel('Full')
    axx.set_ylabel('Quick')

    axx.grid(b=True)

    for ax in [axx, ax1, ax2, ax3, ax4, ax5, ax6, ax1, nx1, axx]: # Don't know why I need to add ax1 again but I have to
        ax.grid()
        ax.set_facecolor('ivory')
        ax.xaxis.set_zorder(10.0)
        ax.yaxis.set_zorder(10.0)


    plt.show()

exit(0)

################################################
################### ATTIC ######################
################################################
# residual sum of squares
# ss_res = np.sum((wave - Func(x, *popt)) ** 2)
            
# total sum of squares
# ss_tot = np.sum((wave - np.mean(wave)) ** 2)
# r-squared
# r2 = 1 - (ss_res / ss_tot

#end = time.time()
#if verbose: print("Fit time:", end-start)
#start = time.time()
#print('!', wave)
#print('?', np.roll(wave, -1))

#_ = ax1.hist(minima, bins=50, color='deeppink', range=(av_min-15, av_min+15))
#ax1.set_title('Pedestal distribution')
#ax1.set_xlabel('ADC ch.')

#    _ = ax2.hist(maxima, bins=20, align='left', range=(min(maxima), max(maxima)) )#, range=(1500, 17000))
#    ax2.set_title('Signal-Pedestal distribution')
#    ax2.set_xlabel('ADC ch.')



#    _ = ax4.hist2d(minima, x_min, bins=(50,50), range=((av_min-15, av_min+15), (min(x_min), max(x_min))), norm=colors.LogNorm(1.0), cmap='PuRd') # PuRd
#    ax4.set_title('Pedestal vs readout No.')
#    ax4.set_xlabel('ADC ch.')
#    ax4.set_ylabel('Readout No.')

# av_min, av_max = np.average(minima), np.average(maxima)

#    _ = ax5.hist2d(maxima, x_max, bins=(20,20), norm=colors.LogNorm(1.0), cmap='PuBuGn')
#    ax5.set_title('Signal-Pedestal vs readout No.')
#    ax5.set_xlabel('ADC ch.')
#    ax5.set_ylabel('Readout No.')

#    print('ax5')


#    ax5.xaxis.set_zorder(10.0)
#    ax5.yaxis.set_zorder(10.0)

#    ax2.xaxis.set_zorder(10.0)
#    ax2.yaxis.set_zorder(10.0)



 #   ax5.grid()
    

#    _ = ax6.hist2d(r2st, ampt, range=((0.4, 1.0), (-0.5, 49.5)), bins=(100,50), norm=colors.LogNorm(1.0), cmap='PuRd')
#    ax6.set_title('R2 of the fit vs signal amplitude')
#    ax6.set_xlabel('R2')
#    ax6.set_ylabel('ADC ch.')
#    ax6.grid()

#    ax6.xaxis.set_zorder(10.0)
#    ax6.yaxis.set_zorder(10.0)

