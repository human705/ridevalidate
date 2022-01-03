import fitdecode
import datetime
import myLogger
import os

# FIT file structure with Dozen Cycle add-on From Garmin Connect
headings = ['timestamp', 'position_lat', 'position_long', 'distance', 'enhanced_altitude', 'altitude', 'enhanced_speed', 'speed',
            'unknown_61', 'unknown_66', 'heart_rate', 'cadence', 'temperature', 'fractional_cadence', 'ePwr', 'GrdPCT', 'nPwr', 'eFTP']

# timestamp: 2021-12-23 16:25:27+00:00
# position_lat: 487418114
# position_long: -874093043
# distance: 200.1
# enhanced_altitude: 45.0
# altitude: 45.0
# enhanced_speed: 5.244
# speed: 5.244
# unknown_61: 2729
# unknown_66: 295
# heart_rate: 118
# cadence: 83
# temperature: 13
# fractional_cadence: 0.0
# ePwr: 66.64624786376953
# %Grd: 2.1860954761505127
# nPwr: 6.016199588775635
# eFTP: 0.0

logger = myLogger.logging.getLogger()


def loadFitToJSON(_myfileName, _myPath):
    logger.info("Building json objects from FIT file: " + _myfileName)
    currentSec = -1
    # rideStartTime = datetime.datetime.utcnow()
    importedSamples = []
    with fitdecode.FitReader(_myPath + '/' + _myfileName) as fit:
        for frame in fit:
            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                if (frame.name == "record"):
                    if (currentSec == -1):
                        currentSec = frame.fields[0].value.timestamp()
                        rideStartTime = datetime.datetime.fromtimestamp(
                            currentSec)
                        d = rideStartTime.strftime("%m/%d/%Y, %H:%M:%S")
                        logger.debug("Debug: Ride start date " + d +
                                     " timestamp: " + str(currentSec))
                        # Adjust for staring point for distance to zero.
                        startingOffset = frame.fields[3].value
                    sampleData = {
                        # EPOCH format seconds
                        "SECS": int(frame.fields[0].value.timestamp() - currentSec),
                        "KM": (frame.fields[3].value - startingOffset) / 1000,
                        # Estimated by Dozen Cycle
                        "WATTS": frame.fields[14].value,
                        "KPH": (frame.fields[7].value * 3.6),
                        "ALT": frame.fields[5].value,
                        "LAT": frame.fields[1].value * (180 / 2 ** 31),
                        "LON": frame.fields[2].value * (180 / 2 ** 31),
                        "HR": frame.fields[10].value,
                        "CAD": frame.fields[11].value,
                        "SLOPE": frame.fields[15].value,
                        "TEMP": frame.fields[12].value,
                    }
                    importedSamples.append(sampleData)
    retObj = {
        "importedSamples": importedSamples,
        "rideStartTime": rideStartTime
    }
    return retObj


def loadFitToList(_myfileName, _myPath):
    # counter = 0
    myRoute = []
    logger.info("Creating a list for FIT file: " + _myfileName)
    with fitdecode.FitReader(_myPath + '/' + _myfileName) as fit:
        for frame in fit:
            # The yielded frame object is of one of the following types:
            # * fitdecode.FitHeader (FIT_FRAME_HEADER) 1
            # * fitdecode.FitCRC (FIT_FRAME_CRC) 2
            # * fitdecode.FitDefinitionMessage (FIT_FRAME_DEFINITION) 3
            # * fitdecode.FitDefinitionMessage (FIT_FRAME_DEFMESG) 3
            # * fitdecode.FitDataMessage (FIT_FRAME_DATA) 4
            # * fitdecode.FitDataMessage (FIT_FRAME_DATAMESG) 4

            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                if (frame.name == "record"):
                    # for j in range(18):
                    #     myTrackPoint.append(0)
                    # print("Precessing frame#: " + str(counter))
                    for i in range(len(frame.fields)):
                        myTrackPoint.append(frame.fields[i].value)
                    myTrackPoint[0] = frame.fields[0].value.timestamp()
                    myTrackPoint[1] = myTrackPoint[1] * (180 / 2 ** 31)
                    myTrackPoint[2] = myTrackPoint[2] * (180 / 2 ** 31)
                    # timeStampEpoch = frame.fields[0].value.timestamp()
                    # myTrackPoint[0] = timeStampEpoch
                    myLogger.debug('timeStamp: ' + str(myTrackPoint[0]))
                    # myDatetime = datetime.datetime.fromtimestamp(myTrackPoint[0])
                    myLogger.debug('datetime: ' +
                                   str(datetime.datetime.fromtimestamp(myTrackPoint[0])))
                    # Add missing fields at the end.
                    # TODO Remove calculated fields from the import process and only import what is needed
                    for j in range(len(myTrackPoint), len(headings)-3):
                        myTrackPoint.append(0)
                    myRoute.append(myTrackPoint)
                    # dic = {headings[i]: myTrackPoint[i]
                    #        for i in range(len(headings))}
                    # json_string = json.dumps(dic, indent=2)
                    # print(json_string)
                    myTrackPoint = []
                    # counter += 1

# Build and return a GC json file from imported information from different type file


def buildGCRideFile(_samplesList, _myfileName, _rideStartTime):
    # Remove original extention
    split_tup = os.path.splitext(_myfileName)
    fn = split_tup[0]
    fe = split_tup[1]
    # Convert date obj to string
    d = _rideStartTime.strftime('%Y/%m/%d %H:%M:%S')
    myMonth = _rideStartTime.strftime('%B')
    myYear = _rideStartTime.strftime('%Y')
    myWeekDay = _rideStartTime.strftime('%A')
    # Create a GC compatible JSON File
    logger.info("Creating a GC file from FIT file: " + _myfileName)
    _importedRide = {
        "RIDE": {
            "STARTTIME": d,
            "RECINTSECS": 1,
            "DEVICETYPE": "custom ",
            "IDENTIFIER": " ",
            "TAGS": {
                "Aerobic TISS": "0 ",
                "Aerobic Training Effect": "0 ",
                "Anaerobic TISS": "0 ",
                "Anaerobic Training Effect": "0 ",
                "Athlete": " ",
                "Average Cadence": "0 ",
                "Average Heart Rate": "0 ",
                "Average Power": "0 ",
                "Average Speed": "0 ",
                "BikeScore™": "0 ",
                "BikeStress": "0 ",
                "CP": "0 ",
                "Change History": " ",
                "Daniels EqP": "0 ",
                "Daniels Points": "0 ",
                "Data": " ",
                "Device": "custom ",
                "Device Info": " ",
                "Distance": "0 ",
                "Duration": "0 ",
                "Elevation Gain": "0 ",
                "Equipment": " ",
                "File Format": " ",
                "Filename": fn + ".json",
                "GOVSS": "0 ",
                "Keywords": "DozenCycle ",
                "LTHR detected": "0 ",
                "LTS detected": "0 ",
                "Month": myMonth,
                "Notes": " ",
                "Objective": " ",
                "Performance Condition": "0 ",
                "Pool Length": "0 ",
                "RPE": "0 ",
                "Recovery Time": "0 ",
                "Route": " ",
                "Source Filename": _myfileName,
                "Sport": " ",
                "SubSport": " ",
                "SwimScore": "0 ",
                "Time Moving": "0 ",
                "VO2max detected": "0 ",
                "Weekday": myWeekDay,
                "Weight": "0 ",
                "Work": "0 ",
                "Workout Code": fn,
                "Year": myYear,
                "xPower": "0 "
            },
            "SAMPLES": _samplesList
        }
    }
    return _importedRide
