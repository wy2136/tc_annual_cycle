#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Fri May 29 16:26:38 EDT 2020
# v2 (2020-10-13): add AM2.5 and AM2.5C360
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
basin = 'NA'
years = slice('1980', '2018')
seed_olife = 12
datafile = __file__.replace('.py', f'.{basin}.nc')
if os.path.exists(datafile):
    ds = xr.open_dataset(datafile)
    print('[loaded]:', datafile)
else:
    from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_ibtracs
    from ERA5.data_pTang_cycle import get_cycle as get_cycle_pERA5
    from ERA5.data_nseed_cycle_rainy import get_cycle as get_cycle_nseedERA5
    from ERA5.data_nseedxp_cycle_rainy import get_cycle as get_cycle_nseedxpERA5
    ds_ntc = get_cycle_ibtracs(basin=basin, years=years)
    ds_p = get_cycle_pERA5(basin=basin, years=years)
    ds_nseed = get_cycle_nseedERA5(basin=basin, years=years).sel(life=seed_olife)
    ds_nseedxp = get_cycle_nseedxpERA5(basin=basin, years=years).sel(life=seed_olife)
    das = dict()
    for src,ds_ in zip(['ntc', 'p', 'nseed', 'nseedxp'], [ds_ntc, ds_p, ds_nseed, ds_nseedxp]):
        for vname in ('mclim', 'cim', 'sem'):
            key = '_'.join([src, vname])
            das[key] = ds_[vname]
    ds = xr.Dataset(das)
    ds.to_netcdf(datafile)
    print('[saved]:', datafile)
 
def wyplot(ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    marker = 'o'
    fillstyle = 'none'
    alpha = 1/4

    labels1 = []
    # IBTrACS TC
    ds_ = ds[['ntc_mclim', 'ntc_cim']].rename(ntc_mclim='mclim', ntc_cim='cim')
    ds_ = ds_/ds_.mclim.sum('month')
    label = 'IBTrACS N_TC'
    labels1.append(label)
    b1 = ax.bar(x='month', height='mclim', data=ds_, label=label)
    ax.errorbar(x='month', y='mclim', yerr='cim', capsize=2, ls='none', color='k', data=ds_, label=None)

    #ERA5 p
    ds_ = ds[['p_mclim', 'p_cim']].rename(p_mclim='mclim', p_cim='cim')
    ds_ = ds_/ds_.mclim.sum('month')
    label = 'ERA5 p($\Lambda$)'
    labels1.append(label)
    color = 'C1'
    ls = '--'
    ds_['lower'] = ds_.mclim - ds_.cim
    ds_['upper'] = ds_.mclim + ds_.cim
    ax.fill_between(x='month', y1='lower', y2='upper', data=ds_, color=color, alpha=alpha, zorder=10)
    ln1 = ds_.mclim.plot(ax=ax, color=color, label=label, marker=marker, ls=ls, fillstyle=fillstyle)

    #ERA5 nseed
    ds_ = ds[['nseed_mclim', 'nseed_cim']].rename(nseed_mclim='mclim', nseed_cim='cim')
    ds_ = ds_/ds_.mclim.sum('month')
    label = 'ERA5 N_SEED'
    labels1.append(label)
    color = 'C2'
    ls = ':'
    ds_['lower'] = ds_.mclim - ds_.cim
    ds_['upper'] = ds_.mclim + ds_.cim
    ax.fill_between(x='month', y1='lower', y2='upper', data=ds_, color=color, alpha=alpha, zorder=10)
    ln2 = ds_.mclim.plot(ax=ax, color=color, label=label, marker=marker, ls=ls, fillstyle=fillstyle)

    #ERA5 nseed x p
    ds_ = ds[['nseedxp_mclim', 'nseedxp_cim']].rename(nseedxp_mclim='mclim', nseedxp_cim='cim')
    ds_ = ds_/ds_.mclim.sum('month')
    label = 'ERA5 N_SEED$\\times$p($\Lambda$)'
    labels1.append(label)
    color = 'C3'
    ds_['lower'] = ds_.mclim - ds_.cim
    ds_['upper'] = ds_.mclim + ds_.cim
    ax.fill_between(x='month', y1='lower', y2='upper', data=ds_, color=color, alpha=alpha, zorder=10)
    ln3 = ds_.mclim.plot(ax=ax, color=color, label=label, marker=marker, fillstyle=fillstyle)
    # move the bar legend to the first (default is the last)
    handles, labels = ax.get_legend_handles_labels()
    handles = handles[-1:-2:-1] + handles[0:-1]
    labels = labels[-1:-2:-1] + labels[0:-1]
    ax.legend(handles, labels)


    ylabel = f'{basin} TC relative frequency'
    title_loc = 'left'
    ax.set_ylim(0, 0.45)
    ax.set_ylabel(ylabel)
    ax.set_xticks(range(1,13))
    #ax.set_xlabel('')
    ax.set_title('')
    #ax.set_title('Obs.', loc=title_loc)
    ax.text(0,1, 'Obs.', ha='left', va='bottom', transform=ax.transAxes)#, fontweight='bold')

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    wyplot()

    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)

    tt.check(f'**Done**')
    plt.show()
    
