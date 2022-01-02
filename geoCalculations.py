import math


def geoDistance(_lat1, _lon1, _lat2, _lon2):
    # _d1 = math.sin(trkpt_array[pt][0]*math.pi/180) * \``
    #     math.sin(trkpt_array[pt+1][0]*math.pi/180)
    # _d2 = math.cos(trkpt_array[pt][0]*math.pi/180)*math.cos(trkpt_array[pt+1][0]*math.pi/180) * \
    #     math.cos(trkpt_array[pt+1][1]*math.pi /
    #                 180-trkpt_array[pt][1]*math.pi/180)
    # if ((_d1 + _d2 >= -1) and (_d1 + _d2 <= 1)):
    #     _d3 = math.acos(_d1 + _d2) * 6371000
    # else:
    #     _d3 = math.acos((d1 + d2) // 1) * 6371000

    # logger.debug("lon1:  " + str(_lon1) + " lat1: " + str(_lat1))

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

    # const R = 6371e3; // metres
    # const φ1 = lat1 * Math.PI/180; // φ, λ in radians
    # const φ2 = lat2 * Math.PI/180;
    # const Δφ = (lat2-lat1) * Math.PI/180;
    # const Δλ = (lon2-lon1) * Math.PI/180;

    # const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
    #         Math.cos(φ1) * Math.cos(φ2) *
    #         Math.sin(Δλ/2) * Math.sin(Δλ/2);
    # const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

    # const d = R * c; // in metres


def geoBearing(_lat1, _lon1, _lat2, _lon2):
    # TO DO

    # Formula:	θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
    # where	φ1,λ1 is the start point, φ2,λ2 the end point (Δλ is the difference in longitude)
    # JavaScript:
    # (all angles in radians)
    # const y = Math.sin(λ2-λ1) * Math.cos(φ2);
    # const x = Math.cos(φ1)*Math.sin(φ2) -
    #         Math.sin(φ1)*Math.cos(φ2)*Math.cos(λ2-λ1);
    # const θ = Math.atan2(y, x);
    # const brng = (θ*180/Math.PI + 360) % 360; // in degrees
    R = 6371000  # metres
