#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed May 27 15:19:27 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#from ERA5.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_era5
#from amipHadISST.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_amipHadISST
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
basin = 'NA'
datafile = __file__.replace('.py', f'.{basin}.nc')
#load data file for the figure if exists; calculate and save the data if not
if os.path.exists(datafile):
    ds = xr.open_dataset(datafile)
    print('[loaded]:', datafile)
else:
    from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_ibtracs
    from amipHadISST.data_ntc_cycle import get_cycle as get_cycle_amipHadISST
    from ERA5.data_pTang_cycle import get_cycle as get_cycle_pTang_era5
    from amipHadISST.data_pTang_cycle import get_cycle as get_cycle_pTang_amipHadISST
    ds_ntc_obs = get_cycle_ibtracs(basin=basin)
    ds_ntc_hiram = get_cycle_amipHadISST(basin=basin)
    ds_p_obs = get_cycle_pTang_era5(basin=basin)
    ds_p_hiram = get_cycle_pTang_amipHadISST(basin=basin)
    das = dict()
    for src,ds_ in zip(['ntc_obs', 'ntc_hiram', 'p_obs', 'p_hiram'], [ds_ntc_obs, ds_ntc_hiram, ds_p_obs, ds_p_hiram]):
        for vname in ('mclim', 'cim', 'sem'):
            da = ds_[vname]
            key = '_'.join([src, vname])
            das[key] = da
    ds = xr.Dataset(das)
    ds.to_netcdf(datafile)
    print('[saved]:', datafile)

def wyplot(ax=None):
    if ax is None:
        figsize = None#(6,3)
        fig,ax = plt.subplots(figsize=figsize)

    label = 'IBTrACS N_TC'
    #ds = get_cycle_ibtracs(basin=basin)
    ds_ = ds[['ntc_obs_mclim', 'ntc_obs_cim']].rename(ntc_obs_mclim='mclim', ntc_obs_cim='cim')
    b1 = ax.bar(x='month', height='mclim', align='edge', width=-0.4, color='0.3', data=ds_, label=label)
    ax.errorbar(data=ds_.assign_coords(month=ds.month-0.2), x='month', y='mclim', yerr='cim', capsize=2, ls='none', color='k', label=None, alpha=1/2)
 
    label = 'HiRAM N_TC'
    #ds = get_cycle_amipHadISST(basin=basin)
    ds_ = ds[['ntc_hiram_mclim', 'ntc_hiram_cim']].rename(ntc_hiram_mclim='mclim', ntc_hiram_cim='cim')
    b2 = ax.bar(x='month', height='mclim', align='edge', width=0.4, color='C0', data=ds_, label=label)
    ax.errorbar(data=ds_.assign_coords(month=ds.month+0.2), x='month', y='mclim', yerr='cim', capsize=2, ls='none', color='k', label=None, alpha=1/2)

    ax_right = ax.twinx()
    label = 'ERA5 p (right)'
    #ds = get_cycle_pTang_era5(basin=basin)#.pipe(lambda x: x.assign_coords(month=x.month-0.2))
    ds_ = ds[['p_obs_mclim', 'p_obs_cim']].rename(p_obs_mclim='mclim', p_obs_cim='cim')
    ds_['lower'] = ds_['mclim'] - ds_['cim']
    ds_['upper'] = ds_['mclim'] + ds_['cim']
    ax_right.fill_between(data=ds_, x='month', y1='lower', y2='upper', alpha=1/4, color='k')
    l1 = ax_right.plot('month', 'mclim', data=ds_, color='k', label=label, marker='o', fillstyle='none')

    label = 'HiRAM p (right)'
    #ds = get_cycle_pTang_amipHadISST(basin=basin)#.pipe(lambda x: x.assign_coords(month=x.month+0.2))
    ds_ = ds[['p_hiram_mclim', 'p_hiram_cim']].rename(p_hiram_mclim='mclim', p_hiram_cim='cim')
    ds_['lower'] = ds_['mclim'] - ds_['cim']
    ds_['upper'] = ds_['mclim'] + ds_['cim']
    ax_right.fill_between(data=ds_, x='month', y1='lower', y2='upper', alpha=1/4, color='C0')
    l2 = ax_right.plot('month', 'mclim', data=ds_, color='C0', label=label, marker='o', fillstyle='none')

    ax.set_ylim(0, None)
    #ax.legend(loc='upper left', frameon=False)
    ax.set_xlabel('month')
    ax.set_ylabel('TC # monthly climatology')
    ax.set_xticklabels(range(1, 13))
    #ax.text(0, 1, '(a)', ha='left', va='bottom', transform=ax.transAxes)#, fontsize='large')
    #ax.text(0, 1, 'a ', ha='right', va='bottom', transform=ax.transAxes, fontweight='bold')

    ax_right.set_ylim(0, None)
    ax_right.set_xticks(range(1, 13))
    ax_right.set_xticklabels(range(1, 13))
    lbs = [b1, b2] + l1 + l2
    labels = [lb.get_label() for lb in lbs]
    ax_right.legend(lbs, labels, loc='upper left')
    #ax_right.set_xlabel('month')
    ax_right.set_ylabel('p')
    ax.set_xlabel('month')

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    wyplot()

    figname = __file__.replace('.py', f'.png')
    if len(sys.argv)>1 and sys.argv[1] == 'savefig':
        wysavefig(figname)
    #print('[saved]:', figname)
    tt.check(f'**Done**')
    plt.show()
    
