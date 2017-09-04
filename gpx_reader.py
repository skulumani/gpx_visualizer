import gpxpy
import gpxpy.gpx
import numpy as np
import pdb
import math as math

import pandas as pd

sec_flag = False

def format_time(time_s):
    if not time_s:
        return 'n/a'
    elif sec_flag:
        return str(int(time_s))
    else:
        minutes = math.floor(time_s / 60.)
        hours = math.floor(minutes / 60.)
        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))


def print_gpx_part_info(gpx_part, indentation='    '):
    """
    gpx_part may be a track or segment.
    """
    length_2d = gpx_part.length_2d()
    length_3d = gpx_part.length_3d()
    print('{}Length 2D: {:.3f}km'.format(indentation, length_2d / 1000.))
    print('{}Length 3D: {:.3f}km'.format(indentation, length_3d / 1000.))

    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx_part.get_moving_data()
    print('%sMoving time: %s' % (indentation, format_time(moving_time)))
    print('%sStopped time: %s' % (indentation, format_time(stopped_time)))
    #print('%sStopped distance: %sm' % stopped_distance)
    print('{}Max speed: {:.2f}m/s = {:.2f}km/h'.format(indentation, max_speed if max_speed else 0, max_speed * 60. ** 2 / 1000. if max_speed else 0))

    uphill, downhill = gpx_part.get_uphill_downhill()
    print('{}Total uphill: {:.2f}m'.format(indentation, uphill))
    print('{}Total downhill: {:.2f}m'.format(indentation, downhill))

    start_time, end_time = gpx_part.get_time_bounds()
    print('%sStarted: %s' % (indentation, start_time))
    print('%sEnded: %s' % (indentation, end_time))

    points_no = len(list(gpx_part.walk(only_points=True)))
    print('%sPoints: %s' % (indentation, points_no))

    if points_no > 0:
        distances = []
        previous_point = None
        for point in gpx_part.walk(only_points=True):
            if previous_point:
                distance = point.distance_2d(previous_point)
                distances.append(distance)
            previous_point = point
        print('{}Avg distance between points: {:.2f}m'.format(indentation, sum(distances) / len(list(gpx_part.walk()))))

    print('')

def print_gpx_info(gpx, gpx_file):
    print('File: %s' % gpx_file)

    if gpx.name:
        print('  GPX name: %s' % gpx.name)
    if gpx.description:
        print('  GPX description: %s' % gpx.description)
    if gpx.author_name:
        print('  Author: %s' % gpx.author_name)
    if gpx.author_email:
        print('  Email: %s' % gpx.author_email)

    print_gpx_part_info(gpx)

    for track_no, track in enumerate(gpx.tracks):
        for segment_no, segment in enumerate(track.segments):
            print('    Track #%s, Segment #%s' % (track_no, segment_no))
            print_gpx_part_info(segment, indentation='        ')

def parse_gpx(gpx_file_name):
    return gpxpy.parse(gpx_file_name)


def data_frame_for_track_segment(segment):
    seg_dict = {}

    for point in segment.points:
        seg_dict[point.time] = [point.latitude, point.longitude,
                                point.elevation, point.speed]
    seg_frame = pd.DataFrame(data=seg_dict)
    # Switch columns and rows s.t. timestamps are rows and gps data columns.
    seg_frame = seg_frame.T
    seg_frame.columns = ['latitude', 'longitude', 'altitude', 'speed']
    return seg_frame


def track_segment_mapping(track):
    segments = [data_frame_for_track_segment(segment)
                for segment in track.segments]
    return segments


def pandas_data_frame_for_gpx(gpx):
    tracks_frames = [track_segment_mapping(track) for track in gpx.tracks]
    # Create a hierarchical DataFrame by unstacking.
    tracks_frame = pd.DataFrame(tracks_frames)
    unstacked_frame = tracks_frame.unstack()
    unstacked_frame.index.name = 'tracks'
    assert gpx.name
    d_frame = pd.DataFrame({gpx.name: unstacked_frame}).T
    d_frame.index.name = 'name'
    return d_frame

# Parse an existing file
filename = 'Morning_Ride.gpx'
gpx_file = open(filename, 'r')
gpx = gpxpy.parse(gpx_file)
dt = gpx.time
time_stamp = int('{:{dfmt}{tfmt}}'.format(dt, dfmt='%Y%m%d', tfmt='%H%M'))
print(time_stamp)
pdb.set_trace()

print_gpx_info(gpx,filename)
# print some info about the gpx file

# for track in gpx.tracks:
#     for segment in track.segments:
#         for point in segment.points:
#             pdb.set_trace()
