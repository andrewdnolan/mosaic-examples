#!/usr/bin/env python3

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import mosaic
import numpy as np
import xarray as xr

from pathlib import Path

mali_mesh = "mpas.gis4to40km"
mali_file = "gis_4to40km.20250214.nc"

mpaso_mesh = "IcoswISC30E3r5"
mpaso_file = "mpaso.IcoswISC30E3r5.rstFromG-chrysalis.20231121.nc"

e3sm_dir = Path("/global/cfs/cdirs/e3sm/inputdata/")

mali_path = e3sm_dir / "glc/mpasli" / mali_mesh / mali_file
mpaso_path = e3sm_dir / "ocn/mpas-o" / mpaso_mesh / mpaso_file

mali_ds = xr.open_dataset(mali_path).squeeze()
icos_ds = xr.open_dataset(mpaso_path).squeeze()
icos_ds.attrs["is_periodic"] = "NO"

latCell = np.rad2deg(icos_ds.latCell)
lonCell = np.rad2deg(icos_ds.lonCell)

latMask = (latCell > 55) & (latCell < 85)
lonMask = (lonCell > 15) & (lonCell < -100)

mask_idxs = icos_ds.nCells.where(latMask | lonMask, drop=True).astype(int)

icos_ds = icos_ds.isel(nCells=mask_idxs)

transform = ccrs.Geodetic()
projection = ccrs.Stereographic(central_latitude=70, central_longitude=-42)

fig = plt.figure(figsize=(7.2, 8), constrained_layout=True)

gs = fig.add_gridspec(10, 3, width_ratios=[0.05, 1, 0.05])

ax = fig.add_subplot(gs[:, 1], projection=projection)

topo_norm = mcolors.TwoSlopeNorm(0, vmin=-2500., vmax=3000)

mali_desc = mosaic.Descriptor(mali_ds, projection, transform, use_latlon=True)
icos_desc = mosaic.Descriptor(icos_ds, projection, transform, use_latlon=True)

ipc = mosaic.polypcolor(ax, icos_desc, icos_ds.indexToCellID, aa=True, ec='k',
                        lw=0.5, cmap='cmo.matter', rasterized=True)

bpc = mosaic.polypcolor(ax, mali_desc, mali_ds.bedTopography,
                        alpha=0.8, aa=True, cmap="cmo.topo",
                        norm=topo_norm, rasterized=True)

hpc = mosaic.polypcolor(ax, mali_desc,
                        mali_ds.thickness.where(lambda x: x > 10.),
                        aa=True, cmap="cmo.ice", rasterized=True)

cax1 = fig.add_subplot(gs[0:5, 2])
fig.colorbar(bpc, cax=cax1, label="Bed Topo. [m a.s.l.]")

cax2 = fig.add_subplot(gs[5:, 2])
fig.colorbar(hpc, cax=cax2, label="Ice Thickness [m]")

cax3 = fig.add_subplot(gs[3:7, 0])
cbar3 = fig.colorbar(ipc, cax=cax3, label="Index to cell ID", shrink=0.5)
cbar3.set_ticks([])
cax3.yaxis.set_label_position('left')

ax.coastlines(lw=0.5)
ax.add_feature(cfeature.LAND)

gl = ax.gridlines(draw_labels=True)
gl.left_labels = True
gl.top_labels = True
gl.bottom_labels = False

ax.set_extent((-60, -25, 58, 84), crs=ccrs.PlateCarree())

fig.savefig(f"figs/{mali_mesh}_with_{mpaso_mesh}.pdf", dpi=500,
            bbox_inches='tight', transparent=True)
plt.close()
