import geoCalculations
# import math


def checkSegmentDist(_current, _prev, _thold):
    rt = -9999
    calcDistDiff = geoCalculations.geoDistance(_prev['LAT'], _prev['LON'], _current['LAT'],
                                               _current['LON'])
    _recordedDist = (_current['KM'] - _prev['KM']) * 1000  # meters
    _check = abs(calcDistDiff - _recordedDist)
    if (_check >= _thold):
        rt = _check
    else:
        rt = 0
    return rt
