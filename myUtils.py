import time
import copy
import math
import pandas as pd
import myLogger

logger = myLogger.logging.getLogger()

# Some records are missing CAD and other info


def AddZerosToEmptyFields(_myData):
    myNewList = []
    data = pd.DataFrame(_myData)
    # Replace any NaN with 0
    data.fillna(0, inplace=True)
    # Convert to list of dict
    myNewList = data.to_dict('records')
    return myNewList


def secToTime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

# Initialize sample point


def initSamplePoint():
    emptyPoint = {
        # EPOCH format seconds
        "SECS": 0,
        "KM": 0,
        "WATTS": 0,
        "KPH": 0,
        "ALT": -999,
        "LAT": -1,
        "LON": -1,
        "HR": -1,
        "CAD": -1,
        "SLOPE": -99,
        "TEMP": -99,
    }
    return emptyPoint

# Convert TCX object to GC


def fromTCXtoGC(_tcxData):
    convertedSamples = []
    samplePoint = initSamplePoint()
    firstTime = True
    rideStartTime = 0
    for point in _tcxData:
        if 'time' in point:
            if firstTime:
                rideStartTime = int(point['time'].timestamp())
                firstTime = False
            samplePoint["SECS"] = int(
                point['time'].timestamp()) - rideStartTime
        if 'distance' in point:
            samplePoint["KM"] = float(
                point['distance'] / 1000)  # GC expects KM
        if 'Watts' in point:
            samplePoint["WATTS"] = point['Watts']
        else:
            samplePoint.pop('WATTS')
        if 'elevation' in point:
            samplePoint["ALT"] = point['elevation']
        if 'speed' in point:
            samplePoint["KPH"] = float(point['speed'] * 3.6)
        if 'latitude' in point:
            samplePoint["LAT"] = point['latitude']
        if 'longitude' in point:
            samplePoint["LON"] = point['longitude']
        if 'heart_rate' in point:
            samplePoint["HR"] = int(point['heart_rate'])
        else:
            samplePoint.pop('HR')
        if 'cadence' in point:
            samplePoint["CAD"] = int(point['cadence'])
        else:
            samplePoint.pop('CAD')
        if 'Slope' in point:
            samplePoint["SLOPE"] = point['Slope']
        else:
            samplePoint.pop('SLOPE')
        if 'temperature' in point:
            samplePoint["TEMP"] = point['temperature']
        else:
            samplePoint.pop('TEMP')
        convertedSamples.append(samplePoint)
        samplePoint = initSamplePoint()

    retObj = {
        "importedSamples": convertedSamples,
        "rideStartTime": rideStartTime
    }
    return retObj

# Replace NaN with zeros and make HR and CAD integers


def cleanupDict(_dict):
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
    # We are skipping first and last, set them to 0 to avoid NaN
    _samples[0]['SLOPE'] = 0.0
    # _samples[len(_samples)-1]['SLOPE'] = 0.0
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
    # TODO - add code from Steve's sample
    pass
