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
#from data_basin_areas import da as basin_areas
#
if __name__ == '__main__':
    tt.check('end import')
#
#start from here
datafile = __file__.replace('.py', '.nc')
if os.path.exists(datafile):
    ds = xr.open_dataset(datafile)
    print('[loaded]:', datafile)
else:
    from ERA5.fig_scatter_ntc_vs_all_mbasins_rainy import ds as ds_obs #ntc is from IBTrACS in ds_obs
    from amipHadISST.fig_scatter_ntc_vs_all_mbasins_rainy import ds as ds_hiram
    from AM2p5.fig_scatter_ntc_vs_all_mbasins_rainy import ds as ds_floram
    from AM2p5C360.fig_scatter_ntc_vs_all_mbasins_rainy2xvort import ds as ds_floramplus
    """
    basin_area_on = [False, True][0]
    if basin_area_on: #p weighted by basin area, NA area is 1
        ds_obs['p'] = ds_obs['p']*(basin_areas/basin_areas.sel(basin='NA')) # normalized by basin areas, NA area is 1
        ds_hiram['p'] = ds_hiram['p']*(basin_areas/basin_areas.sel(basin='NA')) # normalized by basin areas, NA area is 1
        ds_floram['p'] = ds_floram['p']*(basin_areas/basin_areas.sel(basin='NA')) # normalized by basin areas, NA area is 1
        ds_floramplus['p'] = ds_floramplus['p']*(basin_areas/basin_areas.sel(basin='NA')) # normalized by basin areas, NA area is 1
    """
    # normalize by annual total value
    func_norm = lambda x: x/x.sum('month')
    ds_obs = ds_obs.pipe(func_norm)
    ds_hiram = ds_hiram.pipe(func_norm)
    ds_floram = ds_floram.pipe(func_norm)
    ds_floramplus = ds_floramplus.pipe(func_norm)
    # concatenate data
    ds = xr.concat([ds_obs, ds_hiram, ds_floram, ds_floramplus], dim=pd.Index(['Obs.', 'HiRAM', 'AM2.5', 'AM2.5C360'], name='model'))
    ds.to_netcdf(datafile)
    print('[saved]:', datafile)
ds_ = ds.stack(s=['basin', 'month'])

def scatterplot(x=None, y=None, data=None, ax=None, 
    xlabel=None, ylabel=None, title=None, alpha=0.5, 
    tag=None, scatter_on=True, rg_on=True, **kws):
    if ax is None:
        ax = plt.gca()
    if tag is None:
        tag = ''
    if scatter_on:
        ax.scatter(x=x, y=y, data=data, alpha=0.5, s=20, **kws)
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title, loc='left')

    # linear regression
    if rg_on:
        xx, yy = data[x], data[y]
        rg = yy.linregress.on(xx)
        ax.plot([xx.min(), xx.max()], [rg.predicted.min(), rg.predicted.max()], color='k', ls='--', alpha=.5)
        # text
        if rg.intercept.item()>=0:
            #s = f'{tag}\ny={rg.slope.item():.1f}x $+$ {rg.intercept.item():.3f}\nr$^2$={rg.r.item()**2:.2f}'
            s = f'R$^2$={rg.r.item()**2:.2f}\ny={rg.slope.item():.2f}x$+${rg.intercept.item():.3f}'
        else:
            #s = f'{tag}\ny={rg.slope.item():.1f}x $-$ {-rg.intercept.item():.3f}\nr$^2$={rg.r.item()**2:.2f}'
            s = f'R$^2$={rg.r.item()**2:.2f}\ny={rg.slope.item():.2f}x$-${-rg.intercept.item():.3f}'
        #ax.text(0.02, 1-0.02, s, ha='left', va='top', transform=ax.transAxes)
        ax.text(1-0.0, 0.0, s, ha='right', va='bottom', transform=ax.transAxes, color='k', alpha=0.5)
        ax.text(0.02, 1-0.02, f'{tag}', ha='left', va='top', transform=ax.transAxes)
        #print(rg)

basins = ['NA', 'EP', 'WP', 'NI', 'SI', 'AU', 'SP'] 
 
if __name__ == '__main__':
    from wyconfig import * #my plot settings
    plt.rcParams['figure.constrained_layout.use'] = False
    plt.close()
    #fig, axes = plt.subplots(4, 3, sharey=True, sharex='$ol', figsize=(7.5,6.5))
    fig, axes = plt.subplots(4, 3, sharey=True, sharex=True, figsize=(7,8), dpi=98)
    suptitle = None #'Obs. (IBTrACS TC)'
    #figname = __file__.replace('.py', f'_{tt.today()}.png')
    """
    if basin_area_on:
        figname = figname.replace(f'_{tt.today()}', f'_areaWeighted_{tt.today()}')
    """
    #obs
    #ds = ds_obs.stack(s=['basin', 'month'])
    ds = ds_.sel(model='Obs.')

    ax = axes[0, 0]
    #scatterplot(ax=ax, xlabel='ERA5 p($\Lambda$)', ylabel='IBTrACS N_TC', x='p', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag='(a)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'a ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='p', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[0, 1]
    #scatterplot(ax=ax, xlabel='N_SEED', x='nseed', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag='(b)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'b ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseed', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[0, 2]
    #scatterplot(ax=ax, xlabel='N_SEED$\\times$p($\Lambda$)', x='nseedxp', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag='(c)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'c ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseedxp', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    #ax.text(0.99, 0.01, 'Obs.', transform=ax.transAxes, ha='right', va='bottom')

    #ds = ds_hiram.stack(s=['basin', 'month'])
    ds = ds_.sel(model='HiRAM')
    ax = axes[1, 0]
    #scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='HiRAM N_TC', x='p', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag='(d)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'd ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='p', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[1, 1]
    #scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag='(e)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'e ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseed', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[1, 2]
    #scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag='(f)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'f ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseedxp', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    #ax.text(0.99, 0.01, 'HiRAM', transform=ax.transAxes, ha='right', va='bottom')

    #ds = ds_floram.stack(s=['basin', 'month'])
    ds = ds_.sel(model='AM2.5')
    ax = axes[2, 0]
    #scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='HiRAM N_TC', x='p', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag='(g)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'g ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='p', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[2, 1]
    #scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag='(h)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseed', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'h ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseed', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)

    ax = axes[2, 2]
    #scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag='(i)', color='.99', label=None)
    scatterplot(ax=ax, xlabel=None, x='nseedxp', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'i ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseedxp', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    #ax.text(0.99, 0.01, 'AM2.5', transform=ax.transAxes, ha='right', va='bottom')

    #ds = ds_floramplus.stack(s=['basin', 'month'])
    ds = ds_.sel(model='AM2.5C360')
    ax = axes[3, 0]
    #scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='HiRAM N_TC', x='p', y='ntc', data=ds)
    #scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag='(j)', color='.99', label=None)
    scatterplot(ax=ax, xlabel='p($\Lambda$)', ylabel='N_TC', x='p', y='ntc', data=ds, title=None, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'j ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='p', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    #ax.set_xlim(0, 0.21)
    """
    key = 'p'
    xmax = max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    f = 1.05 #scale factor
    ax.set_xlim(0, xmax*f)
    #ax.plot([0, xmax*f], [0, xmax*f], color='gray', ls='--')
    """

    ax = axes[3, 1]
    #scatterplot(ax=ax, xlabel='N_SEED', x='nseed', y='ntc', data=ds, tag='(k)', color='.99', label=None)
    scatterplot(ax=ax, xlabel='N_SEED', x='nseed', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'k ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseed', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    """
    #ax.set_xlim(0, 50) # key = 'nseed'; max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    key = 'nseed'
    xmax = max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    ax.set_xlim(0, xmax*f)
    """

    ax = axes[3, 2]
    #scatterplot(ax=ax, xlabel='N_SEED$\\times$p($\Lambda$)', x='nseedxp', y='ntc', data=ds, tag='(l)', color='.99', label=None)
    scatterplot(ax=ax, xlabel='N_SEED$\\times$p($\Lambda$)', x='nseedxp', y='ntc', data=ds, tag=None, color='.99', label=None)
    ax.text(0.02, 0.98, 'l ', ha='left', va='top', transform=ax.transAxes, fontweight='bold')
    for basin in basins:
        scatterplot(ax=ax, x='nseedxp', y='ntc', data=ds.sel(basin=basin), rg_on=False, label=basin)
    """
    #ax.set_xlim(0, 6) # key = 'nseedxp'; max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    key = 'nseedxp'
    xmax = max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    ax.set_xlim(0, xmax*f)
    #ax.set_ylim(0,8)
    """
    key = 'ntc'
    #ymax = max( ds_obs[key].max(), ds_hiram[key].max(), ds_floram[key].max(), ds_floramplus[key].max())
    ymax = ds_[key].max()
    f = 1.05 #scale factor
    ax.set_ylim(0, ymax*f)
    ax.set_xlim(0, ymax*f)

    if suptitle is not None:
        fig.suptitle(suptitle)
    plt.tight_layout(rect=[0,0,1-0.02,0.95])
    axes[0, 2].legend(bbox_to_anchor=(1, 1), loc='lower right', frameon=False, borderpad=0, ncol=7)
    theta = 90
    ax = axes[0,2]; ax.text(1.02, 0.5, 'Obs.', transform=ax.transAxes, ha='left', va='center', rotation=theta)
    ax = axes[1,2]; ax.text(1.02, 0.5, 'HiRAM', transform=ax.transAxes, ha='left', va='center', rotation=theta)
    ax = axes[2,2]; ax.text(1.02, 0.5, 'AM2.5', transform=ax.transAxes, ha='left', va='center', rotation=theta)
    ax = axes[3,2]; ax.text(1.02, 0.5, 'AM2.5C360', transform=ax.transAxes, ha='left', va='center', rotation=theta)

    figname = __file__.replace('.py', '.png')
    if len(sys.argv) > 1 and sys.argv[1] == 'savefig':
        wysavefig(figname)

    tt.check(f'**Done**')
    plt.show()
    plt.rcParams['figure.constrained_layout.use'] = True
    
