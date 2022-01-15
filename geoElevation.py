import polyline
import requests
import ast
import sys


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
    if (len(s) % 2 == 0):  # even numbers are OK
        myArray = s.split(',')
        i = 0
        while (i <= len(myArray)-2):
            tempStr = str(myArray[i]+',' + str(myArray[i+1]))
            geoPair = geoConvert(tempStr)
            pairList.append(geoPair)
            i += 2
    else:
        sys.exit('Odd number in the list of lat/lon. Aborting')
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
    # payload = {'key': 'H4hMtRQTggt3nhG8RpbrrQ2m9S4Q48pf',
    #            'shapeFormat': 'raw',
    #            'latLngCollection': '40.85809554,-73.266331712,40.868353145,-73.366283393'}
    fulURL = url + '?' + apikey + '&' + shapeFormatcmp6 + '&' + latLngCollection
    res = requests.get(fulURL).json()

    if (len(res) > 0):
        resultList = res['elevationProfile']
        resultSP = res['shapePoints']
        resultInfo = res['info']
        # print('Answer: %s' % res[0])
    else:
        print('Error: %s' % res.content)

    if resultInfo['statuscode'] == 0:
        for result in resultList:
            print('Elevation: %5.5f' % result['height'])

    print('Done!')


s = '40.732049653,-73.221713752,40.73202543,-73.221841995'
getAltitude(geoEncode(s))
# buildGeoPairs(s)
