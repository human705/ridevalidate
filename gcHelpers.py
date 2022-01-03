import os
import myLogger

logger = myLogger.logging.getLogger()


def buildGCRideShell(_rideStartTime, _keyWords):
    # Remove original extention
    # split_tup = os.path.splitext(_myfileName)
    # fn = split_tup[0]
    # fe = split_tup[1]
    # Convert date obj to string
    d = _rideStartTime.strftime('%Y\\/%m\\/%d %H:%M:%S')
    myMonth = _rideStartTime.strftime('%B')
    myYear = _rideStartTime.strftime('%Y')
    myWeekDay = _rideStartTime.strftime('%A')
    # Create a GC compatible JSON File
    logger.info("Creating a GC file shell.")
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
                "Filename": " ",
                "GOVSS": "0 ",
                "Keywords": _keyWords,
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
                "Source Filename": " ",
                "Sport": " ",
                "SubSport": " ",
                "SwimScore": "0 ",
                "Time Moving": "0 ",
                "VO2max detected": "0 ",
                "Weekday": myWeekDay,
                "Weight": "0 ",
                "Work": "0 ",
                "Workout Code": " ",
                "Year": myYear,
                "xPower": "0 "
            },
            "SAMPLES": " "
        }
    }
    return _importedRide
