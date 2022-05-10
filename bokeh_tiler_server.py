'''
Spin up SpaceNet tiles for use in a Bokeh server.

Requiures the 'tiler' conda environment, as well as a 
cloud optimized geotiff (COG).

Huge thanks to Bane Sullivan (https://localtileserver.banesullivan.com/user-guide/bokeh.html)
for helping make this possible.

Usage:
    conda activate tiler
    cd /path_to_spacenet_tiler/
    bokeh serve --show spacenet_tiler_bokeh.py --args /path_to_spacenet_cog.tif
'''

import sys
from localtileserver import TileClient
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.plotting import figure, curdoc, show
from bokeh.models import (
                          Plot, BoxZoomTool, Range1d,
                          BoxZoomTool, WheelZoomTool, PanTool, 
                          SaveTool, ResetTool, UndoTool, RedoTool,
                          WMTSTileSource
                          )

####################
# plot variables
image_path = sys.argv[1]
plot_width = 1000
toolbar_location = "right" 
lod_threshold = None
title = 'SpaceNet Bokeh Tileserver'
projection = 'EPSG:3857'
####################

# First, create a tile server from local raster file
client = TileClient(image_path)

raster_provider = WMTSTileSource(url=client.get_tile_url(client=True))
bounds = client.bounds(projection=projection)
basemap = get_provider(CARTODBPOSITRON)

# bokeh plot
p = figure(plot_width=plot_width, plot_height=int(0.8*plot_width),
              x_range=(bounds[2], bounds[3]), y_range=(bounds[0], bounds[1]),
              x_axis_type="mercator", y_axis_type="mercator", tools='',
              output_backend="webgl",
              toolbar_location=toolbar_location,
              lod_threshold=lod_threshold)

# add map layers
p.add_tile(basemap)
p.add_tile(raster_provider)

# add title and tools
if title:
    p.title.text = title
wheezeetool = WheelZoomTool()
p.add_tools(PanTool(), wheezeetool, BoxZoomTool(),
               SaveTool(), ResetTool(), UndoTool(), RedoTool())
p.toolbar.active_scroll = wheezeetool

# add plot to document
document = curdoc()
document.add_root(p)
