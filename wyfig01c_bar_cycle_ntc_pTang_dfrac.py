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
datafile = __file__.replace('.py', f'.{basin}.csv')
if os.path.exists(datafile):
    df = pd.read_csv(datafile, index_col=0)
    print('[loaded]:', datafile)
else:
    from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_ibtracs
    from amipHadISST.data_ntc_cycle import get_cycle as get_cycle_amipHadISST
    from ERA5.data_pTang_cycle import get_cycle as get_cycle_pTang_era5
    from amipHadISST.data_pTang_cycle import get_cycle as get_cycle_pTang_amipHadISST
    ds_ntc_obs = get_cycle_ibtracs(basin=basin)
    ds_ntc_model = get_cycle_amipHadISST(basin=basin)
    ds_p_obs = get_cycle_pTang_era5(basin=basin)
    ds_p_model = get_cycle_pTang_amipHadISST(basin=basin)
    dss = [[ds_ntc_obs, ds_p_obs], [ds_ntc_model, ds_p_model]]
    # fraction change from Jul to Aug
    func = lambda x: ( x.mclim.sel(month=8)/x.mclim.sel(month=7) - 1 )
    r = np.zeros(shape=(2,2)) + np.nan
    for i in range(2):
        for j in range(2):
            r[i,j] = dss[i][j].pipe(func).item()
    r = xr.DataArray(r, dims=['source', 'variable'], coords=[['Obs.', 'HiRAM'], ['N_TC', 'p']])
    df = r.rename(source='').transpose().to_pandas()
    df.to_csv(datafile)
    print('[saved]:', datafile)


def wyplot(ax=None):
    if ax is None:
        figsize = None#(6,5)
        fig,ax = plt.subplots(figsize=figsize)
    df.plot.bar(ax=ax, rot=0, color=['.3', 'C0'], hatch='...')
    ax.set_xlabel('')
    #ax.set_ylabel('% change from Jul to Aug')
    ax.set_ylabel('')
    ax.text(0, 1, 'fraction increase from Jul to Aug', ha='left', va='bottom', transform=ax.transAxes)#, fontsize='large')

if __name__ == '__main__':
    from wyconfig import * #my plot settings
    wyplot()
    
    figname = __file__.replace('.py', f'.png')
    if len(sys.argv)>1 and sys.argv[1] == 'savefig':
        wysavefig(figname)
    #print('[saved]:', figname)
    tt.check(f'**Done**')
    plt.show()
    
