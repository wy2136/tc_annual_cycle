#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Wed Apr 22 11:04:47 EDT 2020
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, datetime
import xarray as xr, numpy as np, pandas as pd
import matplotlib.pyplot as plt
#more imports
maindir = '/tigress/wenchang/analysis/seedTC'
if maindir not in sys.path:
    sys.path.append(maindir)
#
if __name__ == '__main__':
    tt.check('end import')

#start from here
dfile = __file__.replace('.py', '.nc')
if os.path.exists(dfile):
    da = xr.open_dataarray(dfile)
    print('[loaded]:', dfile)
else:
    from ERA5.data_omega500Z import da
    da.to_dataset(name='seedindex').to_netcdf(dfile)
    print('[saved]:', dfile)

    
if __name__ == '__main__':
    from wyconfig import *
    years_clim = slice('1980', '2018')

    plt.figure()
    #figname = __file__.replace('.py', f'_{today_s}.png')
    da_ = da.sel(case=['ctl', 'aclimZ', 'aclimOmega']) \
        .assign_coords(case=['CTL', 'use annual mean clim. Z', 'use annual mean clim. $\omega$'])
    da_.sel(time=years_clim).groupby('time.month').mean('time').plot(hue='case', marker='o', fillstyle='none')
    plt.axhline(0, color='gray', ls='--')
    plt.xticks(range(1,13))
    plt.ylabel(r'Pa s$^{-1}$')
    plt.title(r'$-\omega\times$Z averaged over NA from ERA5')
    
    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)

    tt.check('done')
    plt.show()
