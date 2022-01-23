from matplotlib.colors import ListedColormap
import polyline
import requests
import ast
import sys
import myLogger
import json
import time

logger = myLogger.logging.getLogger()


def test():
    encoded = polyline.encode([(40.868353145, -73.366283393),
                               (40.87002961, -73.360476661), (40.873153796,	-73.354199789)], 6)
    print("Encoded: %s", (str(encoded)))
    decoded = polyline.decode(encoded, 6, geojson=False)
    print("Decoded: %s", (str(decoded)))


def geoConvert(d):
    return ast.literal_eval(d)


def buildGeoPairs(s):
    pairList = []
    myArray = s.split(',')
    i = 0
    while (i <= len(myArray)-2):
        tempStr = str(myArray[i]+',' + str(myArray[i+1]))
        geoPair = geoConvert(tempStr)
        pairList.append(geoPair)
        i += 2

    # if (len(s) % 2 == 0):  # even numbers are OK

    # else:
    #     logger.error('Odd number in the list of lat/lon. Aborting')
    #     sys.exit('Odd number in the list of lat/lon. Aborting')
    return pairList


def geoEncode(s):
    pairsList = buildGeoPairs(s)
    return polyline.encode(pairsList, 6, geojson=False)


def geoDecode(d):
    return polyline.decode(d, 6, geojson=False)


def getAltitude(strEncoded):
    url = 'http://open.mapquestapi.com/elevation/v1/profile'
    apikey = 'key=H4hMtRQTggt3nhG8RpbrrQ2m9S4Q48pf'
    shapeFormat = 'shapeFormat=raw'
    shapeFormatcmp6 = 'shapeFormat=cmp6'
    latLngCollection = 'latLngCollection=' + strEncoded
    resultList = []
    newXYZList = []
    newXYZSample = {
        "LAT": -999,
        "LON": -999,
        "ALT": -999
    }
    retObj = {
        "retList": [],
        "retCode": -1,
        "retMsg": ""
    }
    fullURL = url + '?' + apikey + '&' + shapeFormat + '&' + latLngCollection
    response = requests.get(fullURL)
    if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
        res = response.json()
        if (len(res) > 0):
            resultList = res['elevationProfile']
            resultSP = res['shapePoints']
            resultInfo = res['info']
            # print('Answer: %s' % res[0])
        else:
            logger.error('Response Error: %s' % res.content)
            sys.exit('Response Error: %s --- Aborting!' % res.content)
        if resultInfo['statuscode'] == 0:
            ctr = 0
            for result in resultList:
                curLat = res['shapePoints'][ctr]
                curLon = res['shapePoints'][ctr+1]
                ctr += 2
                logger.debug('Elevation: %5.5f for LAT: %6.6f and LON: %6.6f' %
                             (result['height'], curLat, curLon))
                newXYZSample['LAT'] = curLat
                newXYZSample['LON'] = curLon
                newXYZSample['ALT'] = result['height']
                newXYZList.append(newXYZSample)
                newXYZSample = {
                    "LAT": -999,
                    "LON": -999,
                    "ALT": -999
                }
        logger.info('Returning a new XYZ list with %d items.' %
                    (len(newXYZList)))

        # print(newXYZList)
        retObj['retList'] = newXYZList
        retObj['retCode'] = 0
        retObj['retMsg'] = "OK"
        return retObj
    else:
        logger.error('Response Error: %d. Error message: %s' %
                     (response.status_code, response.reason))
        retObj['retList'] = []
        retObj['retCode'] = response.status_code
        retObj['retMsg'] = response.reason
        return retObj


# s = '40.732049653,-73.221713752,40.73202543,-73.221841995'
# getAltitude(geoEncode(s))
# #buildGeoPairs(s)

def getAltForGeoListinSegments(_samples, counter):
    """
    Send the incoming list of latlngs in segments based on counter
    Return: a list of dict with lat, lon, alt
    """
    retObj = {
        "retList": [],
        "retCode": -1,
        "retMsg": ""
    }
    apiBody = {}
    locations = []
    loc = {
        "latitude": -999.999,
        "longitude": -999.999
    }
    coordList = []
    partialList = []
    listProcessed = False
    # samplesProcessed = len(_samples)
    listCounter = 0
    while not listProcessed:
        i = 0
        while listCounter <= len(_samples)-1 and i <= counter-1:
            myLat = _samples[listCounter]['LAT']
            myLon = _samples[listCounter]['LON']
            loc["latitude"] = myLat
            loc["longitude"] = myLon
            locations.append(loc)
            listCounter += 1
            i += 1
            loc = {
                "latitude": -999.999,
                "longitude": -999.999
            }
        apiBody = {"locations": locations}
        # Convert to array of strings with 6 digit precision
        # arr = ["%.6f" % i for i in partialList]
        # Convert to one sting
        # myString = ",".join(str(x) for x in arr)
        # time.sleep(seconds)
        # time.sleep(0.5)
        retObj = getOpenApiAltitude(apiBody)
        if retObj['retCode'] == 0:
            coordList += retObj['retList']
        else:
            listProcessed = True
        # print(coordList)
        apiBody = {}
        locations = []
        if listCounter >= len(_samples):
            listProcessed = True

    if retObj['retCode'] == 0:
        retObj = {
            "retList": coordList,
            "retCode": 0,
            "retMsg": "OK"
        }
    return retObj


def buildGeoListFromSamples(_samples):
    """
    NOT USED
    Create a string from the given latlngs
    return: string
    """
    coordList = []
    for sample in _samples:
        coordList.append(sample['LAT'])
        coordList.append(sample['LON'])
    # Convert to array of strings with 6 digit precision
    arr = ["%.6f" % i for i in coordList]
    # Convert to one sting
    myString = ",".join(str(x) for x in arr)
    logger.info('CoordList created with %d item(s) ' % len(coordList))
    return myString


def buildOpenElevAPIBody(_samples):
    """ NOT USED"""
    apiBody = {}
    locations = []
    loc = {
        "latitude": -999.999,
        "longitude": -999.999
    }
    for sample in _samples:
        loc["latitude"] = sample['LAT']
        loc["longitude"] = sample['LON']
        locations.append(loc)
    apiBody = {"locations": locations}
    # logger.info(apiBody)
    # with open('data/test.json', "w") as write_file:
    #     json.dump(apiBody, write_file, indent=2)
    return apiBody


def getOpenApiAltitude(_body):
    """
    Add Altitude to the Lat Lon pairs in the object passed.
    :return: object with Lat, Lon and Alt
    """
    # testbody = {
    #     'locations': [
    #         {
    #             'latitude': 40.86822926066816,
    #             'longitude': -73.36628406308591
    #         },
    #         {
    #             'latitude': 40.86822926066816,
    #             'longitude': -73.36628406308591
    #         },
    #         {
    #             'latitude': 40.86822926066816,
    #             'longitude': -73.36628406308591
    #         },
    #         {
    #             'latitude': 40.86822926066816,
    #             'longitude': -73.36628406308591
    #         },
    #         {
    #             "latitude": 40.86822926066816,
    #             "longitude": -73.36628406308591
    #         }
    #     ]
    # }
    # testList = []
    url = 'https://api.open-elevation.com/api/v1/lookup'
    headers = {"Content-Type": "application/json; Accept: application/json"}
    #   -H 'Accept: application/json' \
    #   -H 'Content-Type: application/json' \
    # Opening JSON file
    # with open('data/test.json') as json_file:
    #     filedata = json.load(json_file)
    # if ('locations' in _body):
    #     testList = _body['locations']

    data = _body
    # data = testList
    # data = testbody
    # data = filedata

    # data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, json=data)

    # print("Status Code", response.status_code)
    # print("JSON Response ", response.json())
    if response.status_code >= 200 and response.status_code <= 299:
        retObj = {
            "retList": response.json()['results'],
            "retCode": 0,
            "retMsg": "Open Elevation API Response: %s  - %s" % (str(response.status_code), response.reason)
        }
        logger.info("Open Elevation API Response: %s  - %s" %
                    (str(response.status_code), response.reason))
    else:
        retObj = {
            "retList": [],
            "retCode": response.status_code,
            "retMsg": response.json()
        }
        logger.error("Open Elevation API Response: %s  - %s" %
                     (str(response.status_code), response.reason))
    return retObj


def replaceElevationValues(_samples, _xyz):

    if (len(_samples) == len(_xyz)):
        cnt = 0
        while cnt <= len(_samples) - 1:
            newAltitude = _xyz[cnt]['elevation']
            _samples[cnt]['ALT'] = newAltitude
            cnt += 1
    else:
        logger.error(
            "Original and new elevation samples are not equal in size.")

    return _samples


def processSamples(_samples):
    # postBoby = buildOpenElevAPIBody(_samples)
    logger.info("Getting Altitude data fro. OpenAltitude API")
    retObj = getAltForGeoListinSegments(_samples, 1000)

    if retObj['retCode'] == 0:
        newObj = replaceElevationValues(_samples, retObj['retList'])
        retObj = {
            "retList": newObj,
            "retCode": 0,
            "retMsg": "OK"
        }

    return retObj
