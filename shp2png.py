import os
import sys
import mapnik # for drawing 
from osgeo import ogr # for open shapefile

shp_path = sys.argv[1]
X = int(sys.argv[2])
Y = int(sys.argv[3])
if X <= 0 or Y <= 0:
    print('Image size should be positive')
    exit()

layer_type = 'pt'
if sys.argc > 4:
    layer_type = sys.argv[4]
if layer_type != 'pt' or layer_type != 'pl' or layer_type != 'pg':
    print('layer type should be one of pt, pl and pg')
    exit()

xmin = xmax = ymin = ymax = None
if sys.argc > 5:
    xmin = float(sys.argv[4])
    xmax = float(sys.argv[5])
    ymin = float(sys.argv[6])
    ymax = float(sys.argv[7])


def render_img(width, height, layer, output, minx, miny, maxx, maxy, layer_type):
  m = mapnik.Map(width, height)
  s = mapnik.Style()

  r = mapnik.Rule()
  symbolizer = None
  if layer_type == "pt":
      print('not implement!') 
      return
  elif layer_type == "pl":
      symbolizer = mapnik.LineSymbolizer()
      symbolizer.stroke = mapnik.Color('#ff0000')
      symbolizer.width = 0.3
  elif layer_type == "pg":
      symbolizer = mapnik.PolygonSymbolizer()
      symbolizer.fill =  mapnik.Color('#ff0000')
  else:
      return
  r.symbols.append(symbolizer)

  s.rules.append(r)
  m.append_style('style', s)

  mlayer = mapnik.Layer(str("test_layer"))
  print('layer param: ', layer)
  mlayer.datasource = mapnik.Shapefile(file=layer)
  mlayer.styles.append('style')

  m.layers.append(mlayer)
  tile_bounds = (minx, miny, maxx, maxy)
  box = mapnik.Box2d(*tile_bounds)
  m.zoom_to_box(box)

  print(output)
  mapnik.render_to_file(m, output)


ds = ogr.Open(shp_path) 
layer = ds.GetLayer(0)
if xmin is None:
    xmin, xmax, ymin, ymax = layer.GetExtent()

render_img(X, Y, shp_path, 'out.png', xmin, ymin, xmax, ymax, layer_type)