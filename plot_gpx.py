import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import pdb
import webbrowser           # open html file

from os import listdir
from os.path import isfile, join


def map_generator(lat_array, lon_array, center_lat, center_lon, zoom):

    with open('map_style') as f:
        style_lines = f.readlines()

    # center_lat = 38.919130
    # center_lon = -77.082370
    # zoom = 11
    # lat_array = [38.926, 38.925463, 38.925467]
    # lon_array = [-77.056689, -77.05669, -77.056686]

    map_html = open('map.html', 'w')

    for i, line in enumerate(style_lines):
        if i==26:
            line = '\t\t\tcenter: {{lat:{}, lng: {}}},\n'.format(center_lat, center_lon)
        elif i==27:
            line = '\t\t\tzoom: {},\n'.format(zoom)
        elif i==288:
            for lat, lon in zip(lat_array, lon_array):
                line = '\t\t\tnew google.maps.LatLng({}, {}),\n'.format(lat, lon)
                map_html.write(line)
            line = ''

        map_html.write(line)

    map_html.close()


def plot_ride(filename):
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    # pdb.set_trace()

    lat = []
    lon = []
    ele = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
                ele.append(point.elevation)

    # fig = plt.figure(facecolor = '0.05')
    # ax = plt.Axes(fig, [0., 0., 1., 1.], )
    # ax.set_aspect('equal')
    # ax.set_axis_off()
    # fig.add_axes(ax)
    # plt.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)

    map_generator(lat, lon, np.mean(lat),  np.mean(lon), 13)
    webbrowser.open('map.html')

    plt.show()


def plot_many_rides(data_path):
    # data_path = 'lpq'
    data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

    lat = []
    lon = []

    fig = plt.figure(facecolor = '0.05')
    ax = plt.Axes(fig, [0., 0., 1., 1.], )
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.add_axes(ax)

    for activity in data:
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
        plt.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)
        lat = []
        lon = []

    filename = data_path + '.png'
    plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)


# plot_ride('Morning_Ride.gpx')
plot_many_rides('./gpx_files')
