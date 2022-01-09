import math
import copy
import myLogger

logger = myLogger.logging.getLogger()

# M in GC Total Mass kg
# TODO - Read from config file?
hRider = 1.72
massTotal = 72.6 + 7.7
Crr = 0.0050
CrEff = Crr
CdA = 0.321
Rho = 1.226
dtLoss = 2  # Drive train % loss
CdANotSet = False
cCad = .002
afCd = 0.62
adipos = math.sqrt(massTotal/(hRider*750))
afSin = 0.89
afCdBike = 1.2
afCATireV = 1.1
afCATireH = 0.9
afAFrame = 0.048
ATire = 0.031
CwaBike = afCdBike * (afCATireV * ATire + afCATireH * ATire + afAFrame)
DraftM = 0.7  # Group ride coeficient. Set to 1 for ridding alone
afCm = 1.025
gConst = 9.8067


def calcPowerGC(_rideSamples):
    logger.info("Calculating power based on GC method.")
    newSamples = copy.deepcopy(_rideSamples)
    CdA = 0.321
    for pt in range(1, len(newSamples)-1):
        prev = newSamples[pt-1]
        current = newSamples[pt]
        next = newSamples[pt+1]
        # TODO - Calculate rider bearing
        # TODO - Calculate absolute wind speed
        windSpeed = 0  # W in GC
        if (current['CAD'] > 0):
            # TODO - Add temperature reading
            # if (ride->areDataPresent()->temp) T = p->temp;
            T = 0
            # TODO - Calculate slope rather than reading from file
            # Calculate power
            # Use recorded slope
            slope = math.atan(current['SLOPE']/100)
            # Cyclist speed m/s plus Wind speed
            V = current['KPH'] * 0.27777777777778
            CrDyn = 0.1 * math.cos(slope)

            Ka = 0
            Frg = gConst * massTotal * \
                (CrEff * math.cos(slope) + math.sin(slope))
            windSpeed = 0  # W in GC
            vw = V+windSpeed  # Wind speed against cyclist = cyclist speed + wind speed

            if (CdANotSet):
                CwaRider = (1 + current['CAD'] * cCad) * afCd * \
                    adipos * (((hRider - adipos) * afSin) + adipos)
                CdA = CwaRider + CwaBike

            Ka = 176.5 * math.exp(-current['ALT']
                                  * .0001253) * CdA * DraftM / (273 + T)

            deltaSpeed = (current['KPH'] - prev['KPH']) / 3.6
            deltaTime = current['SECS'] - prev['SECS']
            accel = 0  # p->kphd
            if (deltaTime > 0):
                accel = deltaSpeed / deltaTime
            # if accel > 1:
            #     accel = 1
            # else:
            #     accel = accel * V * massTotal
            accelPower = accel * V * massTotal

            watts = (afCm * V * (Ka * (vw * vw) + Frg + V * CrDyn)) + accelPower
            # ride->command->setPointValue(i, RideFile::watts, watts > 0 ? (watts > 1000 ? 1000 : watts) : 0);
            logger.debug("Watts: " + str(watts))
        else:
            # No power produced by rider
            watts = 0
        if (watts < 0):
            watts = 0
        current['WATTS'] = watts

    # Apply smoothing
    smoothPoints = 3
    # initialise rolling average
    rtot = 0
    # for (int i=smoothPoints; i>0 && ride->dataPoints().count()-i >=0; i--) {
    #     rtot += ride->dataPoints()[ride->dataPoints().count()-i]->watts;
    # }

    # range(start, end, step)
    # It has the same syntax as python lists where the start is inclusive but the end is exclusive.
    # So if you want to count from 5 to 1, you would use range(5,0,-1) and if you wanted to count from last to posn you would use range(last, posn - 1, -1)

    for i in range(smoothPoints, len(newSamples), -1):
        rtot += newSamples[i]['WATTS']

    logger.debug("rtot: " + str(rtot))
    # //// now run backwards setting the rolling average
    # //for (int i=ride->dataPoints().count()-1; i>=smoothPoints; i--) {
    # //    double here = ride->dataPoints()[i]->watts;
    # //    ride->dataPoints()[i]->watts = rtot / smoothPoints;
    # //    if (ride->dataPoints()[i]->watts<0) ride->dataPoints()[i]->watts = 0;
    # //        rtot -= here;
    # //        rtot += ride->dataPoints()[i-smoothPoints]->watts;
    # //}

    return (newSamples)


def calcPowerGribble(_rideSamples):
    logger.info("Calculating power based on Gribble method.")
    newSamples = copy.deepcopy(_rideSamples)
    badPoints = 0
    for pt in range(1, len(newSamples)-1):
        prev = newSamples[pt-1]
        current = newSamples[pt]
        next = newSamples[pt+1]
        # TODO - Calculate rider bearing
        # TODO - Calculate absolute wind speed
        windSpeed = 0  # W in GC
        if (current['CAD'] > 0):
            # TODO - Add temperature reading
            # if (ride->areDataPresent()->temp) T = p->temp;
            T = 0
            # TODO - Calculate slope rather than reading from file
            # Calculate power
            # Use recorded slope
            slope = math.atan(current['SLOPE']/100)
            # Cyclist speed m/s plus Wind speed
            V = (current['KPH'] * 0.27777777777778) + windSpeed
            fGravity = gConst * math.sin(math.atan(slope)) * massTotal
            fRolling = gConst * math.cos(math.atan(slope)) * massTotal * Crr
            fDrag = 0.5 * CdA * V * V * Rho
            fdtLoss = (1 - (dtLoss / 100))
            fResistance = fGravity + fRolling + fDrag
            # Acceleration
            deltaSpeed = (current['KPH'] - prev['KPH']) / 3.6
            deltaTime = current['SECS'] - prev['SECS']
            accel = 0
            if (deltaTime > 0):
                accel = deltaSpeed / deltaTime
            accelPower = accel * V * massTotal
            # Always subtract acceleration or deceleration power
            if (accelPower > 0):
                accelPower = accelPower * -1
            watts = (fdtLoss * fResistance * V) + accelPower
            # ride->command->setPointValue(i, RideFile::watts, watts > 0 ? (watts > 1000 ? -1 : watts) : 0);
        else:
            # No power produced by rider
            watts = 0
        if (watts < 0):
            watts = 0
        current['WATTS'] = watts
    return (newSamples)
