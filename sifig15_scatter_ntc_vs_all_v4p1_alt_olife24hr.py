#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Jun  4 11:50:59 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob
import xarray as xr, numpy as np, pandas as pd
import matplotlib.pyplot as plt
#more imports
import xaddon
from wyshared import scatterplot
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
    from ERA5.fig_scatter_ntc_vs_all_rainy_olife24hr import get_scatter_data as get_scatter_data_era5
    from IBTrACS.data_ntc_cycle import get_cycle as cycle_ntc
    from amipHadISST.fig_scatter_ntc_vs_all_rainy_olife24hr import get_scatter_data as get_scatter_data_hiram
    from AM2p5.fig_scatter_ntc_vs_all_rainy_olife24hr import get_scatter_data as get_scatter_data_floram
    from AM2p5C360.fig_scatter_ntc_vs_all_rainy2xvort_olife24hr import get_scatter_data as get_scatter_data_floramplus
    ds_obs = get_scatter_data_era5(basin=basin, years=years)
    ds_obs['ntc_era5'] = ds_obs['ntc']
    ds_obs['ntc'] = cycle_ntc(basin=basin, years=years)['mclim']
    ds_hiram = get_scatter_data_hiram(basin=basin, years=years)
    ds_floram = get_scatter_data_floram(basin=basin, years=years)
    ds_floramplus = get_scatter_data_floramplus(basin=basin, years=years)
    # normalize by annual total value
    func_norm = lambda x: x/x.sum('month')
    ds_obs = ds_obs.pipe(func_norm)
    ds_hiram = ds_hiram.pipe(func_norm)
    ds_floram = ds_floram.pipe(func_norm)
    ds_floramplus = ds_floramplus.pipe(func_norm)
    # concatenate data
    ds = xr.concat([ds_obs.drop('ntc_era5'), ds_hiram, ds_floram, ds_floramplus], dim=pd.Index(['Obs.', 'HiRAM', 'AM2.5', 'AM2.5C360'], name='model'))
    ds.to_netcdf(dfile)
    print('[saved]:', dfile)
models = ds.model.values
ds = ds.stack(s=['model', 'month'])
    
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    plt.rcParams['figure.constrained_layout.use'] = False
    plt.close()
    #fig, axes = plt.subplots(4, 3, sharey=True, sharex='col', figsize=(7.5,6.5))
    fig, axes = plt.subplots(1, 3, sharey=True, sharex=True, figsize=(7.5,3))
    suptitle = None #'Obs. (IBTrACS TC)'
    #figname = __file__.replace('.py', f'_{tt.today()}.png')

    ax = axes[0]
    #scatterplot(ax=ax, xlabel='ERA5 p($\Lambda$)', ylabel='IBTrACS N_TC', x='p', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title='Obs.', tag='(a)')
    scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag='(a)', label=None, color='.99')
    for model in models:
        scatterplot(ax=ax, x='p', y='ntc', data=ds.sel(model=model), rg_on=False, label=model)

    ax = axes[1]
    #scatterplot(ax=ax, xlabel='N_SEED', x='nseed', y='ntc', data=ds)
    scatterplot(ax=ax, xlabel='N_SEED', x='nseed', y='ntc', data=ds, tag='(b)', color='.99', label=None)
    for model in models:
        scatterplot(ax=ax, x='nseed', y='ntc', data=ds.sel(model=model), rg_on=False, label=model)

    ax = axes[2]
    #scatterplot(ax=ax, xlabel='N_SEED$\\times$p($\Lambda$)', x='nseedxp', y='ntc', data=ds)
    scatterplot(ax=ax, xlabel='N_SEED$\\times$p($\Lambda$)', x='nseedxp', y='ntc', data=ds, tag='(c)', color='.99', label=None)
    for model in models:
        scatterplot(ax=ax, x='nseedxp', y='ntc', data=ds.sel(model=model), rg_on=False, label=model)
    key = 'ntc'
    ymax = ds[key].max().item()
    f = 1.05 #scale factor
    ax.set_ylim(0, ymax*f)
    ax.set_xlim(0, ymax*f)

    plt.tight_layout(rect=[0,0,1,0.9])
    axes[2].legend(bbox_to_anchor=(1, 1), loc='lower right', frameon=False, ncol=4, borderpad=0)

    if suptitle is not None:
        fig.suptitle(suptitle)

    if len(sys.argv)>1 and sys.argv[1]=='savefig':
        figname = __file__.replace('.py', '.png')
        wysavefig(figname)

    tt.check(f'**Done**')
    plt.show()
    plt.rcParams['figure.constrained_layout.use'] = True
    
