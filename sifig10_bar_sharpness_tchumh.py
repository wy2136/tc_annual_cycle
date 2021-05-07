#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu Apr  1 12:02:25 EDT 2021
if __name__ == '__main__':
    from misc.timer import Timer
    tt = Timer(f'start {__file__}')
import sys, os.path, os, glob, datetime
import xarray as xr, numpy as np, pandas as pd, matplotlib.pyplot as plt
#more imports
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
basin = 'NA'
dfile = __file__.replace('.py', f'.{basin}.csv')
if os.path.exists(dfile):
    df = pd.read_csv(dfile, index_col=0)
    print('[loaded]:', dfile)
else:
    from IBTrACS.data_ntc_cycle import get_cycle as get_cycle_obs_tc
    from IBTrACS.data_ntc_cycle_hu import get_cycle as get_cycle_obs_hu
    from IBTrACS.data_ntc_cycle_mh import get_cycle as get_cycle_obs_mh
    from AM2p5C360.data_ntc_cycle import get_cycle as get_cycle_model_tc
    from AM2p5C360.data_ntc_cycle_hu import get_cycle as get_cycle_model_hu
    from AM2p5C360.data_ntc_cycle_mh import get_cycle as get_cycle_model_mh
    ds_obs_tc = get_cycle_obs_tc(basin=basin)
    ds_obs_hu = get_cycle_obs_hu(basin=basin)
    ds_obs_mh = get_cycle_obs_mh(basin=basin)
    ds_model_tc = get_cycle_model_tc(basin=basin)
    ds_model_hu = get_cycle_model_hu(basin=basin)
    ds_model_mh = get_cycle_model_mh(basin=basin)
    dss = [[ds_obs_tc, ds_obs_hu, ds_obs_mh], [ds_model_tc, ds_model_hu, ds_model_mh]]
    # ratio of Aug-Oct to Nov-Jul
    func = lambda x: x.mclim.sel(month=slice(8,10)).sum('month')/x.mclim.where((x.month>10)|(x.month<8)).sum('month')
    r = np.zeros(shape=(2,3)) + np.nan
    for ii in range(2):
        for jj in range(3):
            r[ii,jj] = dss[ii][jj].pipe(func).item()
    r = xr.DataArray(r, dims=['source', 'variable'], coords=[['Obs.', 'AM2.5C360'], ['TC', 'HU', 'MH']])
    df = r.rename(source='').transpose().to_pandas()
    df.to_csv(dfile)
    print('[saved]:', dfile)
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    fig, ax = plt.subplots()
    p = df.plot.bar(ax=ax, rot=0, table=np.round(df.T, 1), logy=True)
    ax.set_xlabel('')
    ax.set_xticklabels('')
    ax.get_xaxis().set_visible(False)
    ax.set_ylabel('ratio of Aug-Oct to Nov-Jul')
    p.tables[0].scale(1,1.5)
    
    #savefig
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
