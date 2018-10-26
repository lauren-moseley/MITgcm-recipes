#-------- plotting functions -------------------
import matplotlib.pylab as _plt
import numpy as _np
import cartopy as _cart
from matplotlib import colors as _colors
from gridfill import fill as _fill

from .data_organization import *

# plot ASTE on the best possible projection
def plot_ASTE(dataarray, dict_plt):
    ''' make a plot for ASTE from a xmitgcm dataarray
    '''
    
    # explicit list of keys
    figsize = dict_plt['figsize']
    vmin    = dict_plt['vmin']
    vmax    = dict_plt['vmax']
    cmap    = dict_plt['cmap']
    title   = dict_plt['title']

    fig = _plt.figure(figsize=figsize)
    m = _plt.axes(projection=_cart.crs.Orthographic(central_longitude=-35, central_latitude=40))
    m.add_feature(_cart.feature.LAND, facecolor='0.75')
    gl = m.gridlines(draw_labels=False)
    norm = _colors.Normalize(vmin=vmin, vmax=vmax)
    #contours = _np.arange(vmin,vmax,0.2)
    

    kw = dict(eps=1e-2, relax=0.6, itermax=1e4, initzonal=False,
              cyclic=False, verbose=False)
    
    # first plot the faces without padding
    for f in [1,2,4]:
        lon = dataarray['XC'].sel(face=f).values
        lat = dataarray['YC'].sel(face=f).values
        # fill missing values in lon/lat arrays
        lonplt, converged = _fill(_np.ma.masked_values(lon,0), 1, 0, **kw)
        latplt, converged = _fill(_np.ma.masked_values(lat,0), 1, 0, **kw)
        # mask data where needed
        data = dataarray.sel(face=f).values
        depth= dataarray['Depth'].sel(face=f).values
        mask = _np.full(depth.shape, False)
        mask[_np.where(depth == 0)] = True
        dataplt = _np.ma.masked_array(data=data,mask=mask)
        
        C = m.pcolormesh(lonplt, latplt,
                         dataplt, norm=norm, cmap=cmap,\
                         transform=_cart.crs.PlateCarree())
        
    for f in [3]:
        lon = dataarray['XC'].sel(face=f, i=slice(0,125)).values
        lat = dataarray['YC'].sel(face=f, i=slice(0,125)).values
        # mask data where needed
        data = dataarray.sel(face=f, i=slice(0,125)).values
        depth= dataarray['Depth'].sel(face=f, i=slice(0,125)).values
        mask = _np.full(depth.shape, False)
        mask[_np.where(depth == 0)] = True
        dataplt = _np.ma.masked_array(data=data,mask=mask)
        
        C = m.pcolormesh(lon, lat,
                         dataplt, norm=norm, cmap=cmap,\
                         transform=_cart.crs.PlateCarree())
        
    for f in [5]:
        lon = dataarray['XC'].sel(face=f, i=slice(0,155)).values
        lat = dataarray['YC'].sel(face=f, i=slice(0,155)).values
        # mask data where needed
        data = dataarray.sel(face=f, i=slice(0,155)).values
        depth= dataarray['Depth'].sel(face=f, i=slice(0,155)).values
        mask = _np.full(depth.shape, False)
        mask[_np.where(depth == 0)] = True
        dataplt = _np.ma.masked_array(data=data,mask=mask)
        
        C = m.pcolormesh(lon, lat,
                         dataplt, norm=norm, cmap=cmap,\
                         transform=_cart.crs.PlateCarree())
        
    for f in [0]:
        lon = dataarray['XC'].sel(face=f, j=slice(115,270)).values
        lat = dataarray['YC'].sel(face=f, j=slice(115,270)).values
        # mask data where needed
        data = dataarray.sel(face=f, j=slice(115,270)).values
        depth= dataarray['Depth'].sel(face=f, j=slice(115,270)).values
        mask = _np.full(depth.shape, False)
        mask[_np.where(depth == 0)] = True
        dataplt = _np.ma.masked_array(data=data,mask=mask)
        
        C = m.pcolormesh(lon, lat,
                         dataplt, norm=norm, cmap=cmap,\
                         transform=_cart.crs.PlateCarree())
        if 'cticks' in dict_plt:
            cbar = _plt.colorbar(C, ticks=dict_plt['cticks'], norm=norm, shrink=0.75)
            cbar.ax.set_yticklabels(dict_plt['cticks_labels']) 
        else:
            cbar = _plt.colorbar(C, norm=norm, shrink=0.75)
        
    gl = m.gridlines(draw_labels=False)
    _plt.title(title)

    return fig
        

def plot_ASTE_with_grids(dataarray, dict_plt, dirgrid, facet1_grid='ASTE_FACET1.nc',
                                                       facet3_grid='ASTE_FACET3.nc',
                                                       facet4_grid='ASTE_FACET4.nc',
                                                       facet5_grid='ASTE_FACET5.nc'):
    """ plot ASTE using AC, PAC and ARC grids, dataarray must be 2d (x,y)  """

    # explicit list of keys
    figsize = dict_plt['figsize']
    vmin    = dict_plt['vmin']
    vmax    = dict_plt['vmax']
    cmap    = dict_plt['cmap']
    title   = dict_plt['title']

    varname = dataarray.name
    print(varname)
    print(dataarray)

    fig = _plt.figure(figsize=figsize)
    ax = _plt.axes(projection=_cart.crs.Orthographic(central_longitude=-35, central_latitude=40))
    ax.add_feature(_cart.feature.LAND, facecolor='0.75')

    #gl = ax.gridlines(draw_labels=False)
    #norm = _colors.Normalize(vmin=vmin, vmax=vmax)

    # get the grids
    AC  = build_ACgrid_aste270(facet1_grid=dirgrid+facet1_grid, facet5_grid=dirgrid+facet5_grid)
    PAC = build_PACgrid_aste270(facet4_grid=dirgrid+facet4_grid)
    ARC = build_ARCgrid_aste270(facet3_grid=dirgrid+facet3_grid)

    # regrid the data
    da_AC  = regrid_to_AC( dataarray, AC)
    da_PAC = regrid_to_PAC(dataarray, PAC)
    da_ARC = regrid_to_ARC(dataarray, ARC)

    print(AC)
    print(da_AC[varname].values.max())

    ax.set_global()
#    da_AC[varname].where(da_AC[varname] != 0).plot.pcolormesh(ax=ax, transform=_cart.crs.PlateCarree(),
#                                                              x='XC', y='YC', add_colorbar=True,
#                                                              vmin=vmin, vmax=vmax, cmap=cmap)
#
#    _plt.hold()
#    da_PAC[varname].where(da_PAC[varname] != 0).plot.pcolormesh(ax=ax, transform=_cart.crs.PlateCarree(),
#                                                                x='XC', y='YC', add_colorbar=False,
#                                                                vmin=vmin, vmax=vmax, cmap=cmap)
#
#    _plt.hold()
#    da_ARC[varname].where(da_ARC[varname] != 0).plot.pcolormesh(ax=ax, transform=_cart.crs.PlateCarree(),
#                                                                x='XC', y='YC', add_colorbar=False,
#                                                                vmin=vmin, vmax=vmax, cmap=cmap)

    C1 = ax.pcolormesh(da_AC['XC'].values, da_AC['YC'].values,
                       da_AC[varname].values, vmin=vmin, vmax=vmax, cmap=cmap,
                       transform=_cart.crs.PlateCarree())
                       #da_AC[varname].where(da_AC[varname] != 0).values, vmin=vmin, vmax=vmax, cmap=cmap,\

#    C2 = ax.pcolormesh(da_PAC['XC'].values, da_PAC['YC'].values,
#                       da_PAC[varname].where(da_PAC[varname] != 0).values, vmin=vmin, vmax=vmax, cmap=cmap,
#                       transform=_cart.crs.PlateCarree())

#    C3 = ax.pcolormesh(da_ARC['XC'], da_ARC['YC'],
#                       da_ARC[varname].where(da_ARC[varname] != 0), vmin=vmin, vmax=vmax, cmap=cmap,\
#                       transform=_cart.crs.PlateCarree())
#
    return fig
