#!/usr/bin/env python3

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import matplotlib.pyplot as plt
import mosaic
import xarray as xr

from pathlib import Path

mpaso_mesh = "SOwISC12to30E3r3"
mpaso_file = "mpaso.SOwISC12to30E3r3.interpFrom2p1-anvil.20241023.nc"

e3sm_dir = Path("/global/cfs/cdirs/e3sm/inputdata/")

mpaso_path = e3sm_dir / "ocn/mpas-o" / mpaso_mesh / mpaso_file

data_path = "/pscratch/sd/d/dcomeau/e3sm_scratch/pm-cpu/files_for_demo/20250416.v3.SORRME3r3.CRYO1850-DISMF.alfred2-coldstart.chrysalis.mpaso.hist.am.timeSeriesStatsMonthly.0010-01-01.nc"

data_ds = xr.open_dataset(data_path, decode_timedelta=False).squeeze()
mesh_ds = xr.open_dataset(mpaso_path).squeeze()
mesh_ds.attrs["is_periodic"] = "NO"

# define a map projection for our figure
projection = ccrs.InterruptedGoodeHomolosine(central_longitude=-160)
# define the transform that describes our dataset
transform = ccrs.Geodetic()

# create the figure and a GeoAxis
fig, ax = plt.subplots(figsize=(6.75, 5.25), constrained_layout=True,
                       subplot_kw=dict(projection=projection))

# create descriptor object from the mesh dataset
descriptor = mosaic.Descriptor(
    mesh_ds, projection=projection, transform=transform
)

SST = data_ds.timeMonthly_avg_activeTracers_temperature.isel(nVertLevels=0)

collection = mosaic.polypcolor(ax, descriptor, SST, antialiaseds=False,
                               cmap="cmo.curl", vmin=-2., vmax=32.,
                               rasterized=True)

ax.add_feature(cfeature.LAND)
ax.coastlines(resolution='110m', lw=0.5)

fig.colorbar(collection, label=r"SST [$^\circ$ C]", shrink=0.5)

fig.savefig(f"figs/{mpaso_mesh}_SST.pdf", dpi=400,
            bbox_inches='tight', transparent=True)
plt.close()
