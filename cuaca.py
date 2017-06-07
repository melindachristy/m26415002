from __future__ import print_function
import pandas as pd
import json
import numpy as np
from bokeh.io import save
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    LogTicker,
    ColorBar,
    FixedTicker
)
from bokeh.palettes import Inferno256 as palette
from bokeh.plotting import figure, gridplot
palette.reverse()

with open('IDN_adm_1_province.json') as f:
#with open('IDN_adm_2_kabkota.json') as f:
    data = json.load(f)

xgrid = []
ygrid = []
forecast = []

df = pd.read_csv('20160108.csv')
for index, row in df.iterrows():
    xgrid.append(row[0]-125)  #lat
    ygrid.append(row[1]-392)  #long
    forecast.append(row[2])
    #print(index)
    #print(row[1])
#print(xgrid)
#print(ygrid)

lowlat = np.nanmin(xgrid)
highlat = np.nanmax(xgrid)+1
lowlong = np.nanmin(ygrid)
highlong = np.nanmax(ygrid)+1
print(highlat)
xgridfig = np.arange(lowlat,highlat,0.25);
ygridfig = np.arange(lowlong,highlong,0.25);

#print(ygridfig)

#print(forecast)
for i in range(12):
    propinsi = []
    xs = []
    ys = []

            
    for feature in data['features']:
        if feature['geometry'] != None:
            if feature['geometry']['type'] == 'Polygon':
                nama_provinsi = feature['properties']['NAME_1']
                if nama_provinsi == 'Bangka-Belitung':
                    nama_provinsi = 'Kepulauan Bangka Belitung'
                if nama_provinsi == 'Yogyakarta':
                    nama_provinsi = 'D.I. Yogyakarta'
                if nama_provinsi == 'Irian Jaya Barat':
                    nama_provinsi = 'Papua Barat'
                propinsi.append(nama_provinsi)
                x = []
                y = []
                for coord in feature['geometry']['coordinates'][0]:
                    x.append(coord[0])
                    y.append(coord[1])
                xs.append(x)
                ys.append(y)                
            else: #Multipolygon
                for coords in feature['geometry']['coordinates']:
                    nama_provinsi = feature['properties']['NAME_1']
                    if nama_provinsi == 'Bangka-Belitung':
                        nama_provinsi = 'Kepulauan Bangka Belitung'
                    if nama_provinsi == 'Yogyakarta':
                        nama_provinsi = 'D.I. Yogyakarta'
                    if nama_provinsi == 'Irian Jaya Barat':
                        nama_provinsi = 'Papua Barat'
                    propinsi.append(nama_provinsi)
                    x = []
                    y = []
                    for coord in coords[0]:
                        x.append(coord[0])
                        y.append(coord[1])
                    xs.append(x)
                    ys.append(y)

    source = ColumnDataSource(data=dict(
        x=xs,
        y=ys,
        name=propinsi,
        rate=forecast,
    ))

    TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,save"


    p = figure(
        title='good', tools=TOOLS,
        width=1300, height=600
    )
    #change xaxis ticker & xgrid ticker with fixed-width spacing
    p.xaxis.ticker=FixedTicker(ticks=np.arange(95,141.25,0.25))   #spacing by 5 units from -15 to 200
    p.xgrid.ticker=FixedTicker(ticks=np.arange(95,141.25,0.25))

    #change yaxis ticker & ygrid ticker with fixed-width spacing
    p.yaxis.ticker=FixedTicker(ticks=np.arange(-11,6.25,0.25))   #spacing by 5 units from 0 to 100
    p.ygrid.ticker=FixedTicker(ticks=np.arange(-11,6.25,0.25))
    color_mapper = LogColorMapper(palette=palette)

    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(), border_line_color=None, location=(0,0), label_standoff=12)

    #p.add_layout(color_bar, 'left')


    p.grid.grid_line_color = 'red'

    p.patches('x', 'y', source=source,
               fill_color={'field': 'rate', 'transform': color_mapper},
               fill_alpha=0.7, line_color="black", line_width=0.5)

    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Provinsi", "@name"),
        #("Harga(Rp/100 Kg)", "@rate"),
        ("(Long, Lat)", "($x, $y)"),
    ]
    print(save(p, filename='good' + '.html'))