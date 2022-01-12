import time
import copy
import math
import myLogger

logger = myLogger.logging.getLogger()


def secToTime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def cleanupDisc(_dict):
   # Replace NaN with zeros and make HR and CAD integers
    for item in _dict:
        if 'HR' in item:
            if (math.isnan(item['HR'])):
                item['HR'] = 0
            else:
                item['HR'] = int(item['HR'])

        if 'CAD' in item:
            if (math.isnan(item['CAD'])):
                item['CAD'] = 0
            else:
                item['CAD'] = int(item['CAD'])
    return _dict

# Replace slope from altitude and distance


def replaceSlopeFromData(_samples):
    logger.info("Replacing slope form distance and altitude.")
    # newSamples = []
    # myNewTrackPoint = {}
    oldSlope = 0
    for pt in range(1, len(_samples)-1):
        prev = _samples[pt-1]
        current = _samples[pt]
        next = _samples[pt+1]
        deltaDistance = ((current['KM'] - prev['KM']))
        deltaAltitude = current['ALT'] - prev['ALT']
        if (deltaDistance > 0):
            calcSlope = (deltaAltitude / (deltaDistance * 10))
        else:
            calcSlope = oldSlope
        if (calcSlope > 30 or calcSlope < -30):
            calcSlope = oldSlope
        oldSlope = calcSlope
        # myNewTrackPoint = copy.deepcopy(current)
        # newDict = {"SLOPE1": calcSlope,
        #            "deltaDist": deltaDistance, "deltaAlt": deltaAltitude}
        # myNewTrackPoint.update(newDict)
        # logger.debug(myNewTrackPoint)
        # newSamples.append(myNewTrackPoint)
        current['SLOPE'] = calcSlope

    return _samples

# Calculate slope from elevation and distance


def calcSlopeFromData(_samples):
    logger.info("Calculating slope form distance and altitude.")
    newSamples = []
    myNewTrackPoint = {}
    oldSlope = 0
    for pt in range(1, len(_samples)-1):
        prev = _samples[pt-1]
        current = _samples[pt]
        next = _samples[pt+1]
        deltaDistance = ((current['KM'] - prev['KM']))
        deltaAltitude = current['ALT'] - prev['ALT']
        if (deltaDistance > 0):
            calcSlope = (deltaAltitude / (deltaDistance * 10))

        else:
            calcSlope = oldSlope
        if (calcSlope > 30 or calcSlope < -30):
            calcSlope = oldSlope
        oldSlope = calcSlope
        myNewTrackPoint = copy.deepcopy(current)
        newDict = {"SLOPE1": calcSlope,
                   "deltaDist": deltaDistance, "deltaAlt": deltaAltitude}
        myNewTrackPoint.update(newDict)
        logger.debug(myNewTrackPoint)
        newSamples.append(myNewTrackPoint)

    return newSamples


def calcSlopeFromGeoData():
    logger.info('Here')
