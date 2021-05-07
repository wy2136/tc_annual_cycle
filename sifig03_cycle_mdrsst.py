#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Tue Dec  1 11:52:52 EST 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
from geoplots import mapplot
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
dfile = __file__.replace('.py', '.nc')
if os.path.exists(dfile):
    ds = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    ifile = '/tigress/wenchang/analysis/TC_statmodel/HadISST.sstindex.187001-201912.nc'
    ds = xr.open_dataset(ifile)
    ds.to_netcdf(dfile)
    print('[saved]:', dfile)
 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    ds = ds.sel(time=slice('1980', '2018'))
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    fig, ax = plt.subplots()
    da = ds.sst_mdr.groupby('time.month').mean('time')
    da.plot(ax=ax, marker='o', label='MDR SST', color='C0')
    ax.set_ylabel('$^\circ$C')
    ax.legend(loc='upper left')

    ax_ = ax.twinx()
    da = (ds.sst_mdr - ds.sst_trop).groupby('time.month').mean('time')
    da.plot(ax=ax_, marker='o', fillstyle='none', label='MDR relative SST(right)', color='C1')
    ax_.set_ylabel('$^\circ$C')
    ax_.legend(loc='lower right')
    ax_.set_title('Annual cycles of MDR SST and relative SST from HadISST(1980-2018)')
    ax_.set_xticks(range(1,13))

    
    # plot MDR rectanglar region
    ax_small = fig.add_axes([0.11, 0.5, 0.25, 0.25/100*30*16/9])
    plt.sca(ax_small)
    mapplot(lonlatbox=[360-80, 360-20, 10, 25], lonlatbox_color='C0', fill_continents=True)
    plt.xlim(360-100,360)
    plt.ylim(0,30)
    plt.xticks([])
    plt.yticks([])
    plt.text(360-50, 17.5, 'MDR', ha='center', va='center', color='C0')
    #plt.text(360-80, 10, '80W,10N', ha='right', va='top', fontsize='small', color='C0')
    #plt.text(360-20, 25, '20W,25N', ha='left', va='bottom', fontsize='small', color='C0')



    
    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
