import pdb

with open('temp_map') as f:
    style_lines = f.readlines()

center_lat = 38.919130
center_lon = -77.082370
zoom = 11
for i, line in enumerate(style_lines):
    if i==26:
        line = '\t\t\tcenter: {{lat:{}, lng: {}}},\n'.format(center_lat, center_lon)
    elif i==27:
        line = '\t\t\tzoom: {},\n'.format(zoom)
    elif i==288:
        pdb.set_trace()
