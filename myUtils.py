import time
import copy

import myLogger

logger = myLogger.logging.getLogger()


def secToTime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


# Replace slope from altitude and distance

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
        deltaDistance = ((current['KM'] - prev['KM']) * 1000)
        deltaAltitude = current['ALT'] - prev['ALT']
        if (deltaDistance > 0):
            calcSlope = (deltaAltitude / deltaDistance) * 100
            oldSlope = calcSlope
        else:
            calcSlope = oldSlope
        myNewTrackPoint = copy.deepcopy(current)
        newDict = {"SLOPE1": calcSlope,
                   "deltaDist": deltaDistance, "deltaAlt": deltaAltitude}
        myNewTrackPoint.update(newDict)
        logger.debug(myNewTrackPoint)
        newSamples.append(myNewTrackPoint)

    return newSamples


def calcSlopeFromGeoData():
    logger.info('Here')
