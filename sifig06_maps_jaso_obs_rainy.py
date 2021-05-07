#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Jun 11 16:29:29 EDT 2020
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
dfile = __file__.replace('.py', '.tcgenesis.nc')
if os.path.exists(dfile):
    ib = xr.open_dataarray(dfile)
    print('[loaded]:', dfile)
else:
    from IBTrACS.data_TCgenesis_map_mclim import mclim as ib
    ib.to_dataset(name='tcgenesis').to_netcdf(dfile)
    print('[saved]:', dfile)
dfile = __file__.replace('.py', '.p.nc')
if os.path.exists(dfile):
    p_era5 = xr.open_dataarray(dfile)
    print('[loaded]:', dfile)
else:
    from ERA5.data_pTang_map_mclim import mclim as p_era5
    p_era5.to_dataset(name='p_era5').to_netcdf(dfile)
    print('[saved]:', dfile)
dfile = __file__.replace('.py', '.seed.nc')
if os.path.exists(dfile):
    seed_era5 = xr.open_dataarray(dfile)
    print('[loaded]:', dfile)
else:
    from ERA5.data_seedgenesis_map_mclim_rainy import mclim as seed_era5
    seed_era5.to_dataset(name='seed_era5').to_netcdf(dfile)
    print('[saved]:', dfile)
sel_region = lambda x: x.sel(lon=slice(260, 360), lat=slice(0,30)).where(x.lon+x.lat*35/20>295)
sel_region_r = lambda x: x.sel(lon=slice(260, 360), lat=slice(30,0)).where(x.lon+x.lat*35/20>295) #for ERA5 p

 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    import calendar
    plt.close()
    fig, axes = plt.subplots(4, 3, figsize=(8*1.1,5/3*4), sharex=True, sharey=True, dpi=100)
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    months = range(7, 10+1)
    # columns of IBTrACS
    da = ib.pipe(sel_region)
    levels=2.**np.arange(-4, 1.1, 0.5)
    cmap = 'OrRd'
    cbar_on = False
    label = 'TC gen. density'
    for i,mon in enumerate(months):
        ax = axes[i, 0]
        im = da.sel(month=mon).plot.contourf(ax=ax, cmap=cmap, levels=levels, add_colorbar=cbar_on)
        plt.sca(ax)
        mapplot()
    fig.colorbar(im, ax=axes[:, 0], label=label, orientation='horizontal', shrink=0.9)

    #columns of ERA5 p
    da = p_era5.pipe(sel_region_r)
    levels=np.arange(0, 0.51, 0.05)
    cmap = 'Spectral_r'
    cbar_on = False
    label = 'TC gen. prob.'
    for i,mon in enumerate(months):
        ax = axes[i, 1]
        im = da.sel(month=mon).plot.contourf(ax=ax, cmap=cmap, levels=levels, add_colorbar=cbar_on)
        plt.sca(ax)
        mapplot()
    fig.colorbar(im, ax=axes[:, 1], label=label, orientation='horizontal', shrink=0.9)
    

    #columns of ERA5 seed
    da = seed_era5.pipe(sel_region)
    levels=2.**np.arange(-2-1, 3.1-1, 0.5)
    cmap = 'OrRd'
    cbar_on = False
    label = 'seed gen. density'
    for i,mon in enumerate(months):
        ax = axes[i, 2]
        im = da.sel(month=mon).plot.contourf(ax=ax, cmap=cmap, levels=levels, add_colorbar=cbar_on)
        plt.sca(ax)
        mapplot()
    fig.colorbar(im, ax=axes[:, 2], label=label, orientation='horizontal', shrink=0.9)


    for ax,s in zip(axes.flat,list('abcdefghijkl')):
        ax.set_title('')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.text(0, 0, f' ({s})', transform=ax.transAxes, va='bottom')
    for mon,ax in zip(months, axes[:, 0]):
        #ax.text(1, 1, calendar.month_abbr[mon], ha='right', va='top', transform=ax.transAxes)
        ax.set_ylabel(calendar.month_abbr[mon], rotation=0)
        ax.set_yticks(range(0,31,10))
        ax.set_yticklabels(['0', '', '', '30$^\circ$N'])
    for mon,ax in zip(months, axes[2, :]):
        ax.set_xticks(range(270,361,30))
        ax.set_xticklabels(['90$^\circ$W', '60$^\circ$W', '30$^\circ$E', '0'])

    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)

    tt.check(f'**Done**')
    plt.show()
    
