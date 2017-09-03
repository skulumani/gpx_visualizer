import pdb

with open('map_style') as f:
    style_lines = f.readlines()

center_lat = 38.919130
center_lon = -77.082370
zoom = 11
lat_array = [38.926, 38.925463, 38.925467]
lon_array = [-77.056689, -77.05669, -77.056686]

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
