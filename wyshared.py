#!/usr/bin/env python
# Wenchang Yang (wenchang@princeton.edu)
# Thu May  6 17:21:09 EDT 2021
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
 
if __name__ == '__main__':
    #from wyconfig import * #my plot settings
    
    #savefig
    if 'savefig' in sys.argv:
        figname = __file__.replace('.py', f'.png')
        wysavefig(figname)
    tt.check(f'**Done**')
    plt.show()
    
