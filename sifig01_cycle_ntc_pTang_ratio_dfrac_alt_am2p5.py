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
#from amipHadISST.data_ntc_cycle import get_cycle as get_cycle_amipHadISST
#from amipHadISST.data_pTang_cycle import get_cycle as get_cycle_pTang_amipHadISST
#from ERA5.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_era5
#from amipHadISST.data_pTang_partial_cycle import get_cycle as get_cycle_pTangs_amipHadISST
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
basin = 'NA'
dfile = __file__.replace('.py', f'.{basin}.ntc.obs.nc')
if os.path.exists(dfile):
    ds_ntc_obs = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_ibtracs
    ds_ntc_obs = get_cycle_ibtracs(basin=basin)
    ds_ntc_obs.to_netcdf(dfile)
    print('[saved]:', dfile)
dfile = __file__.replace('.py', f'.{basin}.ntc.am2p5.nc')
if os.path.exists(dfile):
    ds_ntc_model = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    from AM2p5.data_ntc_cycle import get_cycle as get_cycle_am2p5
    ds_ntc_model = get_cycle_am2p5(basin=basin)
    ds_ntc_model.to_netcdf(dfile)
    print('[saved]:', dfile)
dfile = __file__.replace('.py', f'.{basin}.p.obs.nc')
if os.path.exists(dfile):
    ds_p_obs = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    from ERA5.data_pTang_cycle import get_cycle as get_cycle_pTang_era5
    ds_p_obs = get_cycle_pTang_era5(basin=basin)
    ds_p_obs.to_netcdf(dfile)
    print('[saved]:', dfile)
dfile = __file__.replace('.py', f'.{basin}.p.am2p5.nc')
if os.path.exists(dfile):
    ds_p_model = xr.open_dataset(dfile)
    print('[loaded]:', dfile)
else:
    from AM2p5.data_pTang_cycle import get_cycle as get_cycle_pTang_am2p5
    ds_p_model = get_cycle_pTang_am2p5(basin=basin)
    ds_p_model.to_netcdf(dfile)
    print('[saved]:', dfile)
dss = [[ds_ntc_obs, ds_p_obs], [ds_ntc_model, ds_p_model]]
# ratio of ASO to all the other months
func = lambda x: x.mclim.sel(month=slice(8,10)).sum('month')/x.mclim.where((x.month>10)|(x.month<8)).sum('month')
r = np.zeros(shape=(2,2)) + np.nan
for i in range(2):
    for j in range(2):
        r[i,j] = dss[i][j].pipe(func).item()
r = xr.DataArray(r, dims=['source', 'variable'], coords=[['Obs.', 'AM2.5'], ['N_TC', 'p']])
df = r.rename(source='').transpose().to_pandas()
# fraction change from Jul to Aug
func = lambda x: ( x.mclim.sel(month=8)/x.mclim.sel(month=7) - 1 )
r = np.zeros(shape=(2,2)) + np.nan
for i in range(2):
    for j in range(2):
        r[i,j] = dss[i][j].pipe(func).item()
r = xr.DataArray(r, dims=['source', 'variable'], coords=[['Obs.', 'AM2.5'], ['N_TC', 'p']])
df_dAug = r.rename(source='').transpose().to_pandas()


if __name__ == '__main__':
    from wyconfig import * #my plot settings
    plt.close()
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    figsize = (6,5)
    #fig, axes = plt.subplots(2, 1, figsize=figsize)
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(2,2)

    #ax = axes[1]#plot (b) first to avoid damage from df.plot.bar
    ax = fig.add_subplot(gs[1,0])
    df.plot.bar(ax=ax, rot=0, color=['.3', 'C0'], hatch='///')
    ax.set_xlabel('')
    #ax.set_ylabel('ratio of Aug-Oct to Nov-Jul')
    ax.set_ylabel('')
    #ax.text(0, 1, '(b)', ha='left', va='bottom', transform=ax.transAxes, fontsize='large')
    ax.text(0, 1, '(b) ratio of Aug-Oct to Nov-Jul', ha='left', va='bottom', transform=ax.transAxes)#, fontsize='large')

    #ax = axes[2]#plot (b) first to avoid damage from df.plot.bar
    ax = fig.add_subplot(gs[1,1])
    df_dAug.plot.bar(ax=ax, rot=0, color=['.3', 'C0'], hatch='...')
    ax.set_xlabel('')
    #ax.set_ylabel('% change from Jul to Aug')
    ax.set_ylabel('')
    #ax.text(0, 1, '(c)', ha='left', va='bottom', transform=ax.transAxes, fontsize='large')
    ax.text(0, 1, '(c) fraction increase from Jul to Aug', ha='left', va='bottom', transform=ax.transAxes)#, fontsize='large')

    #ax = axes[0]
    ax = fig.add_subplot(gs[0, :])
    label = 'IBTrACS N_TC'
    #ds = get_cycle_ibtracs(basin=basin)
    ds = ds_ntc_obs
    b1 = ax.bar(x='month', height='mclim', align='edge', width=-0.4, color='0.3', data=ds, label=label)
    ax.errorbar(data=ds.assign_coords(month=ds.month-0.2), x='month', y='mclim', yerr='cim', capsize=2, ls='none', color='k', label=None, alpha=1/2)
 
    label = 'AM2.5 N_TC'
    #ds = get_cycle_amipHadISST(basin=basin)
    ds = ds_ntc_model
    b2 = ax.bar(x='month', height='mclim', align='edge', width=0.4, color='C0', data=ds, label=label)
    ax.errorbar(data=ds.assign_coords(month=ds.month+0.2), x='month', y='mclim', yerr='cim', capsize=2, ls='none', color='k', label=None, alpha=1/2)

    ax_right = ax.twinx()
    label = 'ERA5 p (right)'
    #ds = get_cycle_pTang_era5(basin=basin)#.pipe(lambda x: x.assign_coords(month=x.month-0.2))
    ds = ds_p_obs
    ds['lower'] = ds['mclim'] - ds['cim']
    ds['upper'] = ds['mclim'] + ds['cim']
    ax_right.fill_between(data=ds, x='month', y1='lower', y2='upper', alpha=1/4, color='k')
    l1 = ax_right.plot('month', 'mclim', data=ds, color='k', label=label, marker='o', fillstyle='none')

    label = 'AM2.5 p (right)'
    #ds = get_cycle_pTang_amipHadISST(basin=basin)#.pipe(lambda x: x.assign_coords(month=x.month+0.2))
    ds = ds_p_model
    ds['lower'] = ds['mclim'] - ds['cim']
    ds['upper'] = ds['mclim'] + ds['cim']
    ax_right.fill_between(data=ds, x='month', y1='lower', y2='upper', alpha=1/4, color='C0')
    l2 = ax_right.plot('month', 'mclim', data=ds, color='C0', label=label, marker='o', fillstyle='none')

    ax.set_ylim(0, None)
    #ax.legend(loc='upper left', frameon=False)
    ax.set_xlabel('month')
    ax.set_ylabel('TC # monthly climatology')
    ax.set_xticklabels(range(1, 13))
    #ax.text(0, 1, '(a)', ha='left', va='bottom', transform=ax.transAxes, fontsize='large')
    ax.text(0, 1, '(a)', ha='left', va='bottom', transform=ax.transAxes)#, fontsize='large')

    ax_right.set_ylim(0, None)
    ax_right.set_xticks(range(1, 13))
    ax_right.set_xticklabels(range(1, 13))
    lbs = [b1, b2] + l1 + l2
    labels = [lb.get_label() for lb in lbs]
    ax_right.legend(lbs, labels, loc='upper left')
    #ax_right.set_xlabel('month')
    ax_right.set_ylabel('p')


    #plt.tight_layout()
    if len(sys.argv)>1 and sys.argv[1] == 'savefig':
        figname = __file__.replace('.py', '.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
