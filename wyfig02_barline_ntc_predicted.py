#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed May  5 12:11:38 EDT 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
from wyfig02a_barline_cycle_ntc_predicted_obs import wyplot as plot_obs 
from wyfig02b_barline_cycle_ntc_predicted_hiram import wyplot as plot_hiram
from wyfig02c_barline_cycle_ntc_predicted_am2p5 import wyplot as plot_am2p5
from wyfig02d_barline_cycle_ntc_predicted_am2p5c360 import wyplot as plot_am2p5c360
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    fig, axes = plt.subplots(2, 2, figsize=(8, 6*9/16*1.5), sharex=False, sharey=True)

    for ax,plot in zip(axes.flat, [plot_obs, plot_hiram, plot_am2p5, plot_am2p5c360]):
        plot(ax)

    #remove xlabels for panel 1 and 2
    for ax in axes.flat[0:2]:
        ax.set_xlabel('')
    #remove ylabels for panel 2 and 4
    for ax in axes.flat[1::2]:
        ax.set_ylabel('')
    #add panel label
    for ax,label in zip(axes.flat, list('abcd')):
        ax.text(0, 1, f'{label}  ', transform=ax.transAxes, ha='right', va='bottom', fontsize='large', fontweight='bold')
    
    #savefig
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        #figname = __file__.replace('.py', f'.png')
        figname = __file__.replace('.py', f'.pdf')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
