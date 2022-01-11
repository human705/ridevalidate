import csv
import myLogger
import os
import json

logger = myLogger.logging.getLogger()

# Build a GC json file with the same name as the imported file


def writeGCJSONFile(_myPath, _myfileName, _importedRide, _rideStartTime, _altFName):
    # Remove original extention
    split_tup = os.path.splitext(_myfileName)
    fn = split_tup[0]
    fe = split_tup[1]
    myMonth = _rideStartTime.strftime('%m')
    myYear = _rideStartTime.strftime('%Y')
    myDay = _rideStartTime.strftime('%d')
    myHour = _rideStartTime.strftime('%H')
    myMin = _rideStartTime.strftime('%M')
    mySec = _rideStartTime.strftime('%S')
    if (_altFName == ''):
        gcFilename = myYear + '_' + myMonth + '_' + \
            myDay + '_' + myHour + '_' + myMin + '_' + mySec
    else:
        gcFilename = _altFName
    # Write pretty print JSON data to file
    logger.info("Writing JSON file: " + _myPath + '/' + gcFilename + '.json')
    with open(_myPath + '/' + gcFilename + '.json', "w") as write_file:
        json.dump(_importedRide, write_file, indent=2)


def writeCSVFile(_myPath, _myfileName, _importedSamples):
    # logger.info("Writing CSV file")
    # with open(myPath + '/' + myfileName + '.csv', 'w', newline='') as f:
    #     # using csv.writer method from CSV package
    #     write = csv.writer(f)
    #     write.writerow(headings)
    #     write.writerows(myNewRoute)

    # this will return a tuple of name and extension
    split_tup = os.path.splitext(_myfileName)
    fn = split_tup[0]
    fe = split_tup[1]

    logger.info("Writing CSV file: " + _myPath + '/' + fn + '.csv')
    with open(_myPath + '/' + fn + '.csv', 'w', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(_importedSamples[0].keys())
        for row in _importedSamples:
            write.writerow(row.values())
