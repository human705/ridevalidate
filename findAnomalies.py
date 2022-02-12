#! /usr/bin/python3
# find anomalies in GPX or .json file of GC import of activity
import sys
import math
import json
import gpxpy
import pathlib
import datetime
import array

if len(sys.argv) != 3:
    sys.exit(
        "2 command line argument expected, GPX or json activity file name and max slope %")

print("Processing file " + sys.argv[1])

maxslope = float(sys.argv[2])


def geoDistance(_lat1, _lon1, _lat2, _lon2):
    R = 6371000  # metres
    _lat1Rad = _lat1 * math.pi/180  # φ, λ in radians
    _lat2Rad = _lat2 * math.pi/180
    _deltaLat = (_lat2-_lat1) * math.pi/180
    _deltaLon = (_lon2-_lon1) * math.pi/180
    _a = math.sin(_deltaLat/2) * math.sin(_deltaLat/2) + math.cos(_lat1Rad) * \
        math.cos(_lat2Rad) * math.sin(_deltaLon/2) * math.sin(_deltaLon/2)
    _c = 2 * math.atan2(math.sqrt(_a), math.sqrt(1-_a))
    _d = R * _c  # in metres
    return _d

# from https://www.movable-type.co.uk/scripts/latlong.html


def radianstodegrees(r):
    d = r * 180 / math.pi
    return d


def degreestoradians(d):
    r = d * math.pi/180
    return r


def geolocation2xyz(_lat, _lon, _alt):
    a = 6378137.0
    e2 = 6.6943799901377997e-3
    lat = degreestoradians(_lat)
    lon = degreestoradians(_lon)
    alt = _alt
    n = a / math.sqrt(1 - e2 * math.sin(lat)*math.sin(lat))
    dx = ((n + alt)*math.cos(lat)*math.cos(lon))  # ECEF x
    dy = ((n + alt)*math.cos(lat)*math.sin(lon))  # ECEF y
    dz = ((n*(1 - e2) + alt)*math.sin(lat))  # ECEF z
    xyz = [dx, dy, dz]
    return xyz


# From https://github.com/GoldenCheetah/GoldenCheetah/blob/cabe078453cbe8e136b8adf8d4187a5be878671b/src/FileIO/LocationInterpolation.cpp


fileExt = pathlib.Path(sys.argv[1]).suffix
if (fileExt.casefold() == '.json'.casefold()):
    filetype = "JSON"
    # Opening JSON file
    f = open(sys.argv[1], encoding='utf-8-sig')

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    log_pts = data['RIDE']['SAMPLES']
elif (fileExt.casefold() == '.gpx'.casefold()):
    filetype = "GPX"
    # Opening GPX file
    f = open(sys.argv[1], encoding='utf-8-sig')
    gpx = gpxpy.parse(f)
    log_pts = [[]]
    for track in gpx.tracks:
        i = 0
        slope = 0
        slope_next = 0
        for segment in track.segments:
            for point in segment.points:
                if i == 0:
                    start_time = point.time
                delta_time = point.time - start_time
                secs = delta_time.total_seconds()
                log_pts.append({"LAT": point.latitude, "LON": point.longitude,
                               "ALT": point.elevation, "TIME": point.time, "SLOPE": 0.0, "SECS": secs})
                i += 1

    del(log_pts[0])

else:
    sys.exit("Only gpx and json activity files are supported")

# Iterating through the track point list
ctr = 0
dif = 0
bad_pts = 0
maxDE = 0
maxDEpt = 0
tot_dist = 0
tot_dist3D = 0
for pt in range(1, len(log_pts)):
    #    print(pt, log_pts[pt]['SECS'])
    if pt > 0:
        # Previous calculation of distance, requires checking for acos>1 due to precision errors
        #        dist = math.sin(log_pts[pt-1]['LAT']*math.pi/180)*math.sin(log_pts[pt]['LAT']*math.pi/180) + math.cos(log_pts[pt-1]['LAT']*math.pi/180)*math.cos(log_pts[pt]['LAT']*math.pi/180)*math.cos(log_pts[pt]['LON']*math.pi/180-log_pts[pt-1]['LON']*math.pi/180)
        #        dist = math.acos(1 if dist > 1 else dist) * 6371000

        dist = geoDistance(log_pts[pt-1]['LAT'], log_pts[pt-1]
                           ['LON'], log_pts[pt]['LAT'], log_pts[pt]['LON'])
        xyz1 = geolocation2xyz(
            log_pts[pt-1]['LAT'], log_pts[pt-1]['LON'], log_pts[pt-1]['ALT'])
        xyz2 = geolocation2xyz(
            log_pts[pt]['LAT'], log_pts[pt]['LON'], log_pts[pt]['ALT'])
        dist3D = math.sqrt((xyz2[0] - xyz1[0])**2 +
                           (xyz2[1] - xyz1[1])**2 + (xyz2[2] - xyz1[2])**2)
        tot_dist3D += dist3D
        if dist == 0:
            bad_pts += 1
            print("Dist= 0 @ pt " + str(pt) + " SECS " + str(log_pts[pt]['SECS']) + " dEle= " + str(
                log_pts[pt]['ALT'] - log_pts[pt-1]['ALT']) + " Ele-1= " + str(log_pts[pt-1]['ALT']) + " Ele= " + str(log_pts[pt]['ALT']))
        else:
            slope = (log_pts[pt]['ALT'] - log_pts[pt-1]['ALT']) / dist * 100
            tot_dist += dist
            if abs(slope) > maxslope:
                bad_pts += 1

    else:
        slope = 0
        dist = 0
        dist_next = 0

    if pt < len(log_pts) - 1:
     #       dist_next = math.sin(log_pts[pt]['LAT']*math.pi/180)*math.sin(log_pts[pt+1]['LAT']*math.pi/180) + math.cos(log_pts[pt]['LAT']*math.pi/180)*math.cos(log_pts[pt+1]['LAT']*math.pi/180)*math.cos(log_pts[pt+1]['LON']*math.pi/180-log_pts[pt]['LON']*math.pi/180)
     #       dist_next = math.acos(1 if dist_next > 1 else dist_next) * 6371000
        dist_next = geoDistance(
            log_pts[pt]['LAT'], log_pts[pt]['LON'], log_pts[pt+1]['LAT'], log_pts[pt+1]['LON'])
        if dist_next != 0:
            slope_next = (log_pts[pt+1]['ALT'] -
                          log_pts[pt]['ALT']) / dist_next * 100
            delta_elev = log_pts[pt]['ALT'] - (log_pts[pt-1]['ALT'] + dist / (
                dist + dist_next) * (log_pts[pt+1]['ALT'] - log_pts[pt-1]['ALT']))
            if abs(delta_elev) > maxDE:
                maxDE = abs(delta_elev)
                maxDEpt = pt
        else:
            slope_next = 0
    if abs(slope) > maxslope:
        if filetype == 'JSON':
            print("Slope prev/next=%6.2f /%6.2f, SLOPE(frm json))=%6.2f Dist prev/next=%6.3f /%6.3f, Delta E=%6.3f @pt %5d and SECS %s and dist %3.6f" %
                  (slope, slope_next, log_pts[pt]['SLOPE'], dist, dist_next, delta_elev, pt, log_pts[pt]['SECS'], log_pts[pt]['KM']))
        else:
            print("Slope prev/next=%6.2f /%6.2f, Dist prev/next=%6.3f /%6.3f, Delta E=%6.3f @pt %5d and SECS %s, time %s and dist %3.6f" %
                  (slope, slope_next,  dist, dist_next, delta_elev, pt, log_pts[pt]['SECS'], log_pts[pt]['TIME'], log_pts[pt]['KM']))
    ctr += 1

print("Bad pts " + str(bad_pts))
print("Max delta E: %6.2f at point %i" % (maxDE, maxDEpt))
print("Number of activity points: %i, SECS at last point: %i" %
      (len(log_pts), log_pts[pt]['SECS']))
print()
print("Total distance on-the-flat: %6.1f" % (tot_dist))
print("Total distance on-the-slope: %6.1f, %% extra distance %2.1f" %
      (tot_dist3D, (tot_dist3D - tot_dist)/tot_dist*100))

print(filetype)

# Closing file
f.close()
