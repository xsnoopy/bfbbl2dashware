# This is a Python script to convert Betaflight Blackbox telemetry logs and prepare them to
# be used as overlays for Dashware.
# Author Michael - Michael (at) believeinrealty.com
# Version 0.1

import os
import csv
import math
import pathlib


def haversine(lat1, lon1, lat2, lon2):   # Calculating the distance between 2 coordinates
    r = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def average(start, window, line, column_existing, column_average):   # Calculating the moving average
    if line < 1:
        return
    if (line <= window / 2):     # Calculate the moving average when the beginning of the average would be outside
                                 # of the range.
        end = int(line + window / 2)
        window = end - start        #  Calculation of window size
        ave = 0.0
        for x in range(start, end):
            ave = ave + float(csv_reader[x][column_existing])
        ave = round(float(ave / window), 2)
        csv_reader[line].insert(column_average, ave)
        return
    if line < (numrow - window / 2):     # Calculate the moving average when the window is in the range
        end = int(line + window / 2)
        start = int(line - window / 2)
        window = end - start    #  Calculation of window size
        ave = 0.0
        for x in range(start, end):
            ave = ave + float(csv_reader[x][column_existing])
        ave = round(float(ave / window), 2)
        csv_reader[line].insert(column_average, ave)
        return
    if line >= (numrow - window / 2):      # Calculate the moving average when the end of the average would be outside
                                           # of the range.
        end = numrow
        start = line
        window = end - start            #  Calculation of window size
        ave = 0.0
        for x in range(start, end):
            ave = ave + float(csv_reader[x][column_existing])
        ave = round(float(ave / window), 2)
        csv_reader[line].insert(column_average, ave)

def findMin(columnNumber):
    minimum = 10000
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        if line > 0:
            if (minimum > int(csv_reader[int(line)][columnNumber])):
                minimum = int(csv_reader[int(line)][columnNumber])
            line += 1
    return minimum

def findMax(columnNumber):
    maximum = -10000
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue
        if line > 0:
            if (maximum < int(csv_reader[int(line)][columnNumber])):
                maximum = int(csv_reader[int(line)][columnNumber])
            line += 1
    return maximum


""" In the first part of the progam the raw blackbox data gets decoded into a CSV file"""

filenames = os.listdir()  # Read oll files in the directory to find the log file
b = 0
for i in filenames:
    if filenames[b][-3:] == "TXT" or filenames[b][-3:] == "bbl":  # Check for  if last 3 digits of each
        # list items with filenames machtes
        # a betaflight log
        currentfile = filenames[b]
        print("Logfile file found " + currentfile)
        if filenames.count(str(filenames[b][:-3] + "01.csv")) > 0:  # Test if csv file already exists.
            print("CSV file already exists. No conversation necessary.")
        else:
            bbdecode = str(pathlib.Path(__file__).parent.absolute()) + "/blackbox_decode --limits --unit-frame-time s " \
                                                                       "--unit-height m --unit-rotation deg/s " \
                                                                       "--unit-acceleration g --unit-gps-speed kph " \
                                                                       "--merge-gps --declination-dec 7.03 " \
                                                                       "--unit-vbat V --simulate-imu --debug " + \
                       filenames[b]  # Start Blackbox decode
            # with parameters
            os.system(bbdecode)  # Call blackbox_decode
            print("Blackbox converted successful to csv ")
    b += 1  # check next file

# First part done. The blackbox data should be extracted successful.
# Now preparing the CSV file for Dashware.

filenames = os.listdir()  # Read oll files in the directory to find the log file
b = 0
for i in filenames:
    if filenames[b][-3:] == "csv":
        currentfile = filenames[b]
        print("CSV file found, try to import " + currentfile)  # Check for  if last 3 digits of each
        # list items with filenames machtes
        # a csv file
        with open(currentfile) as csv_file:
            csv_reader = list(csv.reader(csv_file, delimiter=','))  # import csv file and create list of csv lines
            numcolumn = len(csv_reader[0])  # determine columns in csv file
            numrow = len(csv_reader)  # determine rows in csv file
            print('\r' "Finding Min and Max Values 0%", end="")
            motor0max = findMax(38)   # Finding Motor0Max
            motor1max = findMax(39)   # Finding Motor1Max
            motor2max = findMax(40)   # Finding Motor2Max
            motor3max = findMax(41)   # Finding Motor3Max
            print('\r' "Finding Min and Max Values 25%", end="")
            motor0min = findMin(38)   # Finding Motor0Min
            motor1min = findMin(39)   # Finding Motor1Min
            motor2min = findMin(40)   # Finding Motor2Min
            motor3min = findMin(41)   # Finding Motor3Min
            motor0range = motor0max - motor0min
            motor1range = motor1max - motor1min
            motor2range = motor2max - motor2min
            motor3range = motor3max - motor3min
            print('\r' "Finding Min and Max Values 50%", end="")
            rcCommand0max = findMax(13)  # Finding rcCommand0Max
            rcCommand1max = findMax(14)  # Finding rcCommand1Max
            rcCommand2max = findMax(15)  # Finding rcCommand2Max
            rcCommand3max = findMax(16)  # Finding rcCommand3Max
            print('\r' "Finding Min and Max Values 75%", end="")
            rcCommand0min = findMin(13)  # Finding rcCommand0Min
            rcCommand1min = findMin(14)  # Finding rcCommand1Min
            rcCommand2min = findMin(15)  # Finding rcCommand2Min
            rcCommand3min = findMin(16)  # Finding rcCommand3Min
            print('\r' "Finding Min and Max Values 100% Finding Max Values done.")
            rcCommand0range = rcCommand0max - rcCommand0min
            rcCommand1range = rcCommand1max - rcCommand1min
            rcCommand2range = rcCommand2max - rcCommand2min
            rcCommand3range = rcCommand3max - rcCommand3min
            rcCommand0center = 1500
            rcCommand1center = 1500
            rcCommand2center = 1500
            rcCommand3center = 1500


            line_count = 0
            for row in csv_reader:
                if (line_count % 1000) == 0:  # Simple progress indication
                    print('\r' "Calculation progress: " + str(round((float(line_count / numrow * 100)), 2)) + "%",
                          end="")
                if line_count == 0:  # Prepare header row
                    csv_reader[line_count].insert(numcolumn + 1, "Time of video (s)")  # Insert Time of video
                    csv_reader[line_count].insert(numcolumn + 2, "Vbat (V)")  # Insert Motor Voltage
                    csv_reader[line_count].insert(numcolumn + 3, "Acceleration total (g)")  # Insert Acceleration
                    csv_reader[line_count].insert(numcolumn + 4, "Total Motor Power (VA)")  # Insert Motor power
                    csv_reader[line_count].insert(numcolumn + 5, "GPS dist home (m)")  # Insert GPS dist home
                    csv_reader[line_count].insert(numcolumn + 6,
                                                  "GPS dist trav (m)")  # Insert GPS distance traveled home
                    csv_reader[line_count].insert(numcolumn + 7,
                                                  "GPS max speed currently (km/h)")  # Insert GPS max speed
                    csv_reader[line_count].insert(numcolumn + 8, "Acceleration max currently (g)")  # Insert Gforece max
                    csv_reader[line_count].insert(numcolumn + 9,
                                                  "Max motor power currently (VA)")  # Insert Motor Power max
                    csv_reader[line_count].insert(numcolumn + 10,
                                                  "Max current currently (A)")  # Insert current draw max
                    csv_reader[line_count].insert(numcolumn + 11, "Min battery Voltage (V)")  # Inser Voltage minimum
                    csv_reader[line_count].insert(numcolumn + 12,
                                                  "Total Motor Power (VA) smooth")  # Insert Motor power smooth
                    csv_reader[line_count].insert(numcolumn + 13,
                                                  "Amperage (A) smooth")  # Insert Amperage smooth
                    csv_reader[line_count].insert(numcolumn + 14,
                                                  "Voltage (V) smooth")  # Insert Battery Voltage smooth
                    csv_reader[line_count].insert(numcolumn + 15,
                                                  "Motor 0 smooth")  # Insert Motor 0 smooth
                    csv_reader[line_count].insert(numcolumn + 16,
                                                  "Motor 1 smooth")  # Insert Motor 1 smooth
                    csv_reader[line_count].insert(numcolumn + 17,
                                                  "Motor 2 smooth")  # Insert Motor 2 smooth
                    csv_reader[line_count].insert(numcolumn + 18,
                                                  "Motor 3 smooth")  # Insert Motor 3 smooth

                if line_count == 1:
                    csv_reader[line_count].insert(numcolumn + 1, float(0.0))  # Time calculation
                    csv_reader[line_count].insert(numcolumn + 2,
                                                  float(csv_reader[line_count][21]) / float(10.0))  # Volatge correction
                    csv_reader[line_count].insert(numcolumn + 3, round(math.sqrt(float(csv_reader[line_count][31]) *
                                                                                 float(csv_reader[line_count][31]) +
                                                                                 float(csv_reader[line_count][32]) *
                                                                                 float(csv_reader[line_count][32]) +
                                                                                 float(csv_reader[line_count][33]) *
                                                                                 float(csv_reader[line_count][33])),
                                                                       2))  # Calculate acceleration
                    csv_reader[line_count].insert(numcolumn + 4, round(float(csv_reader[line_count][numcolumn + 2]) *
                                                                       float(csv_reader[line_count][22]),
                                                                       2))  # Calculate Motor power
                    csv_reader[line_count].insert(numcolumn + 5, "0.0")  # Initial Home distance set to 0
                    csv_reader[line_count].insert(numcolumn + 6, "0.0")  # Initial travel distance set to 0
                    csv_reader[line_count][52] = csv_reader[25][52]  # Copy of a later GPS position to use at home.
                    csv_reader[line_count][53] = csv_reader[25][53]  # Copy of a later GPS position to use at home.
                    csv_reader[line_count].insert(numcolumn + 7, "0.0")  # Initial GPS start speed set to 0
                    csv_reader[line_count].insert(numcolumn + 8, "0.0")  # Initial Gforce max set to 0
                    csv_reader[line_count].insert(numcolumn + 9, "0.0")  # Initial Motor Power max set to 0
                    csv_reader[line_count].insert(numcolumn + 10, "0.0")  # Initial current draw max set to 0
                    csv_reader[line_count].insert(numcolumn + 11, csv_reader[line_count][
                        numcolumn + 1])  # Initial current Voltage max set to start
                    csv_reader[line_count][38] = round(((float(csv_reader[line_count][38]) - motor0min) /
                                                        motor0range) * 100, 1)  # Bring Motor load 0 in range 0 - 100%
                    csv_reader[line_count][39] = round(((float(csv_reader[line_count][39]) - motor1min) /
                                                        motor1range) * 100, 1)  # Bring Motor load 1 in range 0 - 100%
                    csv_reader[line_count][40] = round(((float(csv_reader[line_count][40]) - motor2min) /
                                                        motor2range) * 100, 1)  # Bring Motor load 2 in range 0 - 100%
                    csv_reader[line_count][41] = round(((float(csv_reader[line_count][41]) - motor3min) /
                                                        motor3range) * 100, 1)  # Bring Motor load 3 in range 0 - 100%
                    csv_reader[line_count][13] = round(
                        ((float(csv_reader[line_count][13])) / 5),
                        1)  # Bring rcCommand 0 in range 0 - 100%
                    csv_reader[line_count][14] = round(
                        ((float(csv_reader[line_count][14])) / 5),
                        1)  # Bring rcCommand 1 in range 0 - 100%
                    csv_reader[line_count][15] = round(
                        ((float(csv_reader[line_count][15])) / 5),
                        1)  # Bring rcCommand 2 in range 0 - 100%
                    csv_reader[line_count][16] = round(
                        ((float(csv_reader[line_count][16]) - 1500) / 5),
                        1)  # Bring rcCommand 3 in range 0 - 100%

                if line_count >= 2:
                    csv_reader[line_count].insert(numcolumn + 1, (round(
                        float(csv_reader[line_count][1]) - float(csv_reader[line_count - 1][1]) + float(
                            csv_reader[line_count - 1][numcolumn]), 5)))  # Time calc.
                    csv_reader[line_count].insert(numcolumn + 2, round(float(csv_reader[line_count][21]) / float(10.0),
                                                                       2))  # Volatge correction
                    csv_reader[line_count].insert(numcolumn + 3, round(math.sqrt(float(csv_reader[line_count][31]) *
                                                                                 float(csv_reader[line_count][31]) +
                                                                                 float(csv_reader[line_count][32]) *
                                                                                 float(csv_reader[line_count][32]) +
                                                                                 float(csv_reader[line_count][33]) *
                                                                                 float(csv_reader[line_count][
                                                                                           33])),
                                                                       2))  # Calculate acceleration
                    csv_reader[line_count].insert(numcolumn + 4, round(float(csv_reader[line_count][numcolumn + 1]) *
                                                                       float(csv_reader[line_count][22]),
                                                                       2))  # Calculate Motor power

                    csv_reader[line_count].insert(numcolumn + 5, round((haversine(float(csv_reader[20][52]),
                                                                                  float(csv_reader[20][53]),
                                                                                  float(csv_reader[line_count - 1][52]),
                                                                                  float(
                                                                                      csv_reader[line_count - 1][53]))),
                                                                       2)
                                                  )  # Calculating distance to home using the GPS coordinate form line 20 as the home point
                    csv_reader[line_count].insert(numcolumn + 6,
                                                  round((float(haversine(float(csv_reader[line_count][52]),
                                                                         float(csv_reader[line_count][53]),
                                                                         float(csv_reader[line_count - 1][52]),
                                                                         float(csv_reader[line_count - 1][53]))) +
                                                         float(csv_reader[line_count - 1][numcolumn + 5])), 2)
                                                  )  # Using the GPS coordinate to caclculate distance traveled
                    if float(csv_reader[line_count][55]) > float(
                            csv_reader[line_count - 1][numcolumn + 6]):  # Compare max Gps Speed
                        csv_reader[line_count].insert(numcolumn + 6, csv_reader[line_count][55])
                    else:
                        csv_reader[line_count].insert(numcolumn + 6, csv_reader[line_count - 1][numcolumn + 6])
                    if float(csv_reader[line_count][numcolumn + 2]) > float(
                            csv_reader[line_count - 1][numcolumn + 7]):  # Compare max Geforces
                        csv_reader[line_count].insert(numcolumn + 7, csv_reader[line_count][numcolumn + 2])
                    else:
                        csv_reader[line_count].insert(numcolumn + 7, csv_reader[line_count - 1][numcolumn + 7])
                    if float(csv_reader[line_count][numcolumn + 3]) > float(
                            csv_reader[line_count - 1][numcolumn + 8]):  # Motor Power max
                        csv_reader[line_count].insert(numcolumn + 8, csv_reader[line_count][numcolumn + 3])
                    else:
                        csv_reader[line_count].insert(numcolumn + 8, csv_reader[line_count - 1][numcolumn + 8])
                    if float(csv_reader[line_count][22]) > float(
                            csv_reader[line_count - 1][numcolumn + 9]):  # Current draw max
                        csv_reader[line_count].insert(numcolumn + 10, csv_reader[line_count][22])
                    else:
                        csv_reader[line_count].insert(numcolumn + 10, csv_reader[line_count - 1][numcolumn + 9])
                    if float(csv_reader[line_count][numcolumn + 1]) < float(
                            csv_reader[line_count - 1][numcolumn + 10]):  # Battery Volatge min
                        csv_reader[line_count].insert(numcolumn + 11, csv_reader[line_count][numcolumn + 1])
                    else:
                        csv_reader[line_count].insert(numcolumn + 11, csv_reader[line_count - 1][numcolumn + 10])

                    # Bring Motor readings in 0-100% scale

                    csv_reader[line_count][38] = round(
                        ((float(csv_reader[line_count][38]) - motor0min) / motor0range) * 100,
                        1)  # Bring Motor load 0 in range 0 - 100%
                    csv_reader[line_count][39] = round(((float(csv_reader[line_count][39]) - motor1min) /
                                                        motor1range) * 100, 1)  # Bring Motor load 1 in range 0 - 100%
                    csv_reader[line_count][40] = round(((float(csv_reader[line_count][40]) - motor2min) /
                                                        motor2range) * 100, 1)  # Bring Motor load 2 in range 0 - 100%
                    csv_reader[line_count][41] = round(((float(csv_reader[line_count][41]) - motor3min) /
                                                        motor3range) * 100, 1)  # Bring Motor load 3 in range 0 - 100%

                    # Bring RC Commands in 0-100% scale

                    csv_reader[line_count][13] = round(
                        ((float(csv_reader[line_count][13])) / 5),
                        1)  # Bring rcCommand 0 in range 0 - 100%
                    csv_reader[line_count][14] = round(
                        ((float(csv_reader[line_count][14])) / 5),
                        1)  # Bring rcCommand 1 in range 0 - 100%
                    csv_reader[line_count][15] = round(
                        ((float(csv_reader[line_count][15])) / 5),
                        1)  # Bring rcCommand 2 in range 0 - 100%
                    csv_reader[line_count][16] = round(
                        (((float(csv_reader[line_count][16])) - 1500) / 5),
                        1)  # Bring rcCommand 3 in range 0 - 100%

                line_count += 1
            print(" Calculation process done.")
            line_count = 0
            #  Average of some items in the csv file in order to get smoother gauges.
            for row in csv_reader:
                if (line_count % 1000) == 0:  # Simple progress indication
                    print('\r' "Smoothing progress: " + str(round((float(line_count / numrow * 100)), 2)) + "%",
                          end="")
                window = 40       # Window for average
                average(1, window, line_count, numcolumn + 3, numcolumn + 12)   # Smoothing Total Motor VA
                average(1, window, line_count, 22, numcolumn + 13)              # Smoothing Amperage
                average(1, window, line_count,numcolumn +1, numcolumn + 14)     # Smoothing Battery Voltage
                average(1, window, line_count, 38, numcolumn + 15)              # Smoothing Motor 0
                average(1, window, line_count, 39, numcolumn + 16)              # Smoothing Motor 1
                average(1, window, line_count, 40, numcolumn + 17)              # Smoothing Motor 2
                average(1, window, line_count, 41, numcolumn + 18)              # Smoothing Motor 3
                line_count += 1

        # Last part of program, Write to a new CSV file.
        print(" Smoothing process done.")
        line_count = 0
        with open('{0}_converted.csv'.format(currentfile[:-4]),
                  mode='w') as output_file:  # add _converted to output filename
            output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if (line_count % 1000) == 0:  # Simple progress indication
                    print('\r' "Write to file progress: " + str(round((float(line_count / numrow * 100)), 2)) + "%",
                          end="")
                output_file.writerow(csv_reader[line_count])
                line_count += 1
        print('\n' "Converting of the CSV file successful.")
    b += 1
