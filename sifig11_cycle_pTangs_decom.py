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
#from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_ibtracs
#from amipHadISST.data_ntc_cycle import get_cycle as get_cycle_amipHadISST
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
basin = 'NA'
years = slice('1980', '2018')
dfile = __file__.replace('.py', f'.{basin}.nc')
if os.path.exists(dfile):
    ds = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    #from ERA5.data_pTang_cycle import get_cycle as get_cycle_pTang_era5
    #from amipHadISST.data_pTang_cycle import get_cycle as get_cycle_pTang_amipHadISST
    from ERA5.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_era5
    from amipHadISST.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_amipHadISST
    das = {v:get_cycle_pTangs_era5(basin=basin, years=years, fixterm=v)['mclim'] for v in [None, 'Vshear', 'chi', 'PI']}
    ds_obs = xr.Dataset(das).rename({None: 'nonefixed'})
    das = {v:get_cycle_pTangs_amipHadISST(basin=basin, years=years, fixterm=v)['mclim'] for v in [None, 'Vshear', 'chi', 'PI']}
    ds_hiram = xr.Dataset(das).rename({None: 'nonefixed'})
    ds = xr.concat([ds_obs, ds_hiram], dim=pd.Index(['obs', 'hiram'], name='model'))
    ds.to_netcdf(dfile)
    print('[saved]:', dfile)

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    plt.close()
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    figsize = (6,5)
    fs = 'none'#fillstyle
    fig, axes = plt.subplots(2, 1, figsize=figsize, sharex=True, sharey=True)

    ax = axes[0]
    ds_ = ds.sel(model='obs')
    ds_['nonefixed'].plot(label='ERA5 full', color='k', marker='o', ax=ax, fillstyle=fs)
    ds_['PI'].plot(label='const $u_{PI}$', color='C1', marker='o', ax=ax, fillstyle=fs)
    ds_['chi'].plot(label='const $\chi$', color='C2', marker='o', ax=ax, fillstyle=fs)
    ds_['Vshear'].plot(label='const $u_{shear}$', color='C3', marker='o', ax=ax, fillstyle=fs)

    ax.legend()
    #ax.yaxis.tick_right()
    #ax.yaxis.set_label_position("right")
    ax.set_xlabel('')
    ax.set_ylabel('p')
    #ax.set_ylim(ax_right.get_ylim())
    ax.text(1-0.01, 1-0.02, '(a)', ha='right', va='top', transform=ax.transAxes, fontsize='large')

    ax = axes[1]
    ds_ = ds.sel(model='hiram')
    ds_['nonefixed'].plot(label='HiRAM full', color='C0', marker='o', ax=ax, fillstyle=fs)
    ds_['PI'].plot(label='const $u_{PI}$', color='C1', marker='o', ax=ax, fillstyle=fs)
    ds_['chi'].plot(label='const $\chi$', color='C2', marker='o', ax=ax, fillstyle=fs)
    ds_['Vshear'].plot(label='const $u_{shear}$', color='C3', marker='o', ax=ax, fillstyle=fs)

    ax.legend()
    #ax.yaxis.tick_right()
    #ax.yaxis.set_label_position("right")
    ax.set_xlabel('month')
    ax.set_ylabel('p')
    #ax.set_ylim(ax_right.get_ylim())
    ax.text(1-0.01, 1-0.02, '(b)', ha='right', va='top', transform=ax.transAxes, fontsize='large')

    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
