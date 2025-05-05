import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import mosaic
import numpy as np
import xarray as xr

from pathlib import Path

mpassi_mesh = "IcoswISC30E3r5"
mpassi_file = "mpassi.IcoswISC30E3r5.20231120.nc"

e3sm_dir = Path("/global/cfs/cdirs/e3sm/inputdata/")

mpassi_path = e3sm_dir / "ice/mpas-seaice" / mpassi_mesh / mpassi_file

data_path = "/pscratch/sd/d/dcomeau/e3sm_scratch/pm-cpu/files_for_demo/v3.LR.piControl.mpassi.hist.am.timeSeriesStatsMonthly.0001-01-01.nc"

data_ds = xr.open_dataset(data_path, decode_timedelta=False)
mesh_ds = xr.open_dataset(mpassi_path).squeeze()
mesh_ds.attrs["is_periodic"] = "NO"

# get a mask of norther hemisphere (NH) cell indices
NH_mask = mesh_ds.latCell > 0
NH_idxs = mesh_ds.nCells.where(NH_mask, drop=True).astype(int)

# subset the result to just read in NH data
mesh_ds = mesh_ds.isel(nCells=NH_idxs)
data_ds = data_ds.isel(nCells=NH_idxs).squeeze()

# define a map projection for our figure
projection = ccrs.NorthPolarStereo()
# define the transform that describes our dataset
transform = ccrs.Geodetic()

# create descriptor object from the mesh dataset
descriptor = mosaic.Descriptor(
    mesh_ds, projection=projection, transform=transform
)

# create the figure and a GeoAxis
fig, ax = plt.subplots(1, 1, figsize=(6.5, 4.5), facecolor="w",
                       constrained_layout=True,
                       subplot_kw=dict(projection=projection))

# set data to nan for values less than 15%
concentration = data_ds.timeMonthly_avg_iceAreaCell.where(lambda x: x > 0.15)

collection = mosaic.polypcolor(ax, descriptor, concentration, aa=False,
                               ec='face', cmap="cmo.ice", rasterized=True)

ax.set_extent([-180, 180, 50, 90], ccrs.PlateCarree())

gl = ax.gridlines()
gl.xlocator = mticker.FixedLocator(np.arange(-180., 181., 20.))
gl.ylocator = mticker.FixedLocator(np.arange(-80., 81., 10.))
gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
gl.right_labels = False
gl.left_labels = False
gl.top_labels = True
gl.bottom_labels = True
gl.rotate_labels = False

ax.add_feature(cfeature.LAND)
ax.coastlines(resolution='50m', lw=0.6)

fig.colorbar(collection, label="Sea ice concentration")

fig.savefig(f"figs/{mpassi_mesh}_NH_si-concentration.pdf", dpi=400,
            bbox_inches='tight', transparent=True)
plt.close()
