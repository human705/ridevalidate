# import fitdecode
import csv
import datetime
import sys
import json
import logging

import copy
import pathlib
import pandas as pd

# My modules
import importFIT
import rideChecks
import myUtils
import plotTests
# import geoCalculations
import myExports


# Check to see if we have info to proceed
# We need a file for input. If we get a FIT file we'll convert it to GC JSON before moving on.
# We assume the path is data under the current folder
# 1st arg is the file name
if len(sys.argv) != 2:
    sys.exit("Please include a filename only!")

# Create and configure logger
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        # logging.FileHandler("newfile.log")
                    ])

# Creating a logging object
logger = logging.getLogger()

fileName = sys.argv[1]
filePath = 'data'

# function to return the file extension
fileExt = pathlib.Path(sys.argv[1]).suffix
if (fileExt == ".fit"):
    logging.info("Got a " + fileExt +
                 " file. Importing and converting to json")

    # Process FIT file
    myRetObj = importFIT.loadFitToJSON(fileName, filePath)
    importedSamples = myRetObj['importedSamples']
    rideStartTime = myRetObj['rideStartTime']
    importedRide = importFIT.buildGCRideFile(
        importedSamples, fileName, rideStartTime)
    # Write files
    myExports.buildGCJSONFile(filePath, fileName, importedRide, rideStartTime)
    myExports.buildCSVFile(filePath, fileName, importedSamples)

elif (fileExt == '.json'):
    logging.info("Got a " + fileExt + " file. Moving on.")
    # Read existing GC JSON file
    f = open(filePath + '/' + fileName, encoding='utf-8-sig')
    # f = open('data/2021_12_12_08_56_42.json')
    # returns JSON object as# a dictionary
    data = json.load(f)
    importedSamples = copy.deepcopy(data['RIDE']['SAMPLES'])
    # Closing file
    f.close()
else:
    logging.error('We can only process fit or json files. Aborting...')
    sys.exit("We can only process fit or json files. Aborting...")


# Show plot
# plotTests.testPlotHist(importedSamples)

# Run tests
badPoints = 0
for pt in range(1, len(importedSamples)-1):
    prev = importedSamples[pt-1]
    current = importedSamples[pt]
    next = importedSamples[pt+1]

    # Segment distance based on LAT and LON
    # checkSegmentDist = rideChecks.checkSegmentDist(
    #     current, prev, 5)

    # Time in file from SECS
    # timeMark = myUtils.secToTime(current['SECS'])
    # Speed meters / second from LAT and LON
    # segmentSpeed = ((current['KM'] - prev['KM']) *
    #                 1000) / (current['SECS'] - prev['SECS'])
    # speedDiff = abs(segmentSpeed - (current['KPH'] * 0.2777778))

    # if (speedDiff > 5):
    #     logger.info("Speed variance of " + str(speedDiff) +
    #                 " for time index: " + str(current['SECS']) + " distance: " + str(current['KM']) + ' time: ' + timeMark)

    # if (checkSegmentDist > 0):
    #     logger.info("Distance variance of " + str(checkSegmentDist) +
    #                 " for time index: " + str(current['SECS']) + " distance: " + str(current['KM']) + ' time: ' + timeMark)

    # slopeRun = ((current['KM'] - prev['KM']) * 1000)
    # slopeRise = current['ALT'] - prev['ALT']
    # if (slopeRun > 0):
    #     calcSlope = (slopeRise / slopeRun) * 100
    # else:
    #     calcSlope = 0

    # if ((calcSlope - current['SLOPE']) > 1):
    #     badPoints += 1
    #     logger.info("Slope variance of " + str(calcSlope - current['SLOPE']) + " timeidx: " + str(current['SECS']) +
    #                 " rec slope: " + str(current['SLOPE']) + " calcSlope: " + str(calcSlope) + " @ distance: " + str(current['KM']) + ' time: ' + timeMark)


# ridePoints = []
# ridePoint = []
# for point in importedSamples:
#     ridePoint.append(point['SECS'])
#     ridePoint.append(point['KM'])
#     ridePoint.append(point['WATTS'])
#     ridePoint.append(point['KPH'])
#     ridePoint.append(point['ALT'])
#     ridePoint.append(point['LAT'])
#     ridePoint.append(point['LON'])
#     ridePoint.append(point['HR'])
#     ridePoint.append(point['CAD'])
#     ridePoint.append(point['SLOPE'])
#     ridePoint.append(point['TEMP'])
#     ridePoints.append(ridePoint)
#     ridePoint = []
# logger.info("Created ridepoints list")


# for pt in range(0, len(myRoute)):
#     myNewTrackPoint = []

#     # Calculate distance from Lat and Long
#     if ((pt >= 1) and (pt <= len(myRoute))):
#         calcDistDiff = geoCalculations.geoDistance(myRoute[pt-1][1], myRoute[pt-1]
#                                                    [2], myRoute[pt][1], myRoute[pt][2])
#         # Calculate speed (m/sec from calculated distance and recorded time)
#         calcSpeed = calcDistDiff / (myRoute[pt][0] - myRoute[pt-1][0])
#     else:
#         calcDistDiff = 0
#         calcSpeed = 0

#     totalCalcDist += calcDistDiff
#     myNewTrackPoint = copy.deepcopy(myRoute[pt])
#     myNewTrackPoint.append(calcDistDiff)
#     myNewTrackPoint.append(calcSpeed)
#     myNewTrackPoint.append(totalCalcDist)
#     myNewRoute.append(myNewTrackPoint)


# logger.info('Total points: ' + str(len(importedSamples) + 1))
# logger.info('Bad points = ' + str(badPoints))

# Write Files
# myPath = 'data'
# myfileName = 'Port Jeff Classic'

# Write new files
# if (1 == 0):

#     output = csv.writer(sys.stdout)
#     output.writerow(data[0].keys())  # header row
#     for row in data:
#         output.writerow(row.values())

#     Write pretty print JSON data to file
#     logger.info("Writing JSON file")
#     with open("data/2021_12_12_08_56_42.json", "w") as write_file:
#         json.dump(importedRide, write_file, indent=2)

#     logger.info("Writing CSV file")
#     with open(myPath + '/' + myfileName + '.csv', 'w', newline='') as f:
#         # using csv.writer method from CSV package
#         write = csv.writer(f)
#         write.writerow(headings)
#         write.writerows(myNewRoute)

#     logger.info("Writing CSV file")
#     with open(filePath + '/' + fileName + '.csv', 'w', newline='') as f:
#         # using csv.writer method from CSV package
#         write = csv.writer(f)
#         write.writerow(importedSamples[0].keys())
#         for row in importedSamples:
#             write.writerow(row.values())

logger.info("Done!")