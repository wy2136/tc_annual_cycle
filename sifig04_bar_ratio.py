#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Mon Nov 30 15:22:46 EST 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
#import matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
tag = ['ASO2otherMonths', 'dAugfrac'][1]
if tag == 'ASO2otherMonths':
    f = lambda x: x.sel(month=slice(8,10)).sum('month')/x.where((x.month<8)|(x.month>10)).sum('month')
    long_name = 'ratio of Aug-Oct to Nov-Jul'
    #tag = 'ASO2otherMonths'
elif tag == 'dAugfrac':
    f = lambda x: ( x.sel(month=8)/x.sel(month=7) - 1)
    long_name = 'fraction change from Aug to Jul'
    #tag = 'dAugfrac'
"""
f = lambda x: ( x.sel(month=8)/x.sel(month=7) - 1) * 100
long_name = '% change from Aug to Jul'
tag = 'dAug'
"""
"""
f = lambda x: x.sel(month=8)/x.sel(month=7)
long_name = 'ratio of TC # of Aug to Jul'
tag = 'Aug2Jul'
"""
"""
f = lambda x: x.sel(month=slice(8,10)).sum('month')/x.sum('month')
long_name = 'fraction of Aug-Oct TC #'
tag = 'ASOfrac'
"""
dfile = __file__.replace('.py', f'.{tag}.nc')
if tag == 'dAugfrac':
    dfile = dfile.replace('sifig04', 'sifig05')
if os.path.exists(dfile):
    r = xr.open_dataarray(dfile)
    print('[loaded]:', dfile)
else:
    from fig_scatter_ntc_vs_all_v4p1 import ds_obs, ds_hiram, ds_floram, ds_floramplus # dependent on fig_scatter_ntc_vs_all_v3.py
    
    dss = [ds_obs, ds_hiram, ds_floram, ds_floramplus]
    danames = ['ntc', 'p', 'nseed', 'nseedxp']
    r = np.zeros(shape=(4,4))+np.nan
    for i,ds in enumerate(dss):
        for j,vname in enumerate(danames):
            r[i,j] = ds[vname].pipe(f).item()
    r = xr.DataArray(r, dims=['model', 'predictor'], coords=[['Obs.', 'HiRAM', 'AM2.5', 'AM2.5C360'], ['N_TC', 'p', 'N_seed', r'N_seed$\times$p']])
    r.to_dataset(name=tag).to_netcdf(dfile)
    print('[saved]:', dfile)
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    #figname = __file__.replace('.py', f'_{tag}_{tt.today()}.png')
    figsize = None#6,5
    fig, ax = plt.subplots(figsize=figsize)
    da = r
    #da = da.isel(predictor=slice(-1, None, -1))
    df = da.transpose().to_pandas().rename_axis('', axis=1)
    p = df.plot.bar(ax=ax, rot=0, table=np.round(df.T, 4))

    ax.xaxis.tick_top()
    ax.set_xlabel('')
    ax.set_ylabel(long_name)
    #plt.grid(True)
    ax.get_xaxis().set_visible(False)
    p.tables[0].scale(1,1)


    #print(da)
    
    #plt.tight_layout()
    figname = __file__.replace('.py', f'_{tag}.png')
    if tag == 'dAugfrac':
        figname = figname.replace('sifig04', 'sifig05')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
