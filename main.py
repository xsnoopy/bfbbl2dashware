# This is a Python script to convert Betaflight Blackbox telemetry logs and prepare them to
# be used as overlays for Dashware.
# Author Michael - Michael (at) believeinrealty.com
# Version 0.1

import os
import csv
import math
import pathlib


def haversine(lat1, lon1, lat2, lon2):
    r = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


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

            line_count = 0
            motor0max = 0
            motor1max = 0
            motor2max = 0
            motor3max = 0
            rcCommand0max = 0
            rcCommand1max = 0
            rcCommand2max = 0
            rcCommand3max = 0
            for row in csv_reader:
                if line_count > 1 and line_count < numrow:     # Finding Motor0Max
                        if (motor0max < int(csv_reader[line_count][38])) and line_count + 3 < numrow:
                            motor0max = int(csv_reader[line_count][38])
                if line_count > 1 and line_count < numrow:     # Finding Motor1Max
                        if (motor1max < int(csv_reader[line_count][39])) and line_count + 3 < numrow:
                            motor1max = int(csv_reader[line_count][39])
                if line_count > 1 and line_count < numrow:     # Finding Motor2Max
                        if (motor2max < int(csv_reader[line_count][40])) and line_count + 3 < numrow:
                            motor2max = int(csv_reader[line_count][40])
                if line_count > 1 and line_count < numrow:     # Finding Motor3Max
                        if (motor3max < int(csv_reader[line_count][41])) and line_count + 3 < numrow:
                            motor3max = int(csv_reader[line_count][41])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand0Max
                        if (rcCommand0max < int(csv_reader[line_count][13])) and line_count + 3 < numrow:
                            rcCommand0max = int(csv_reader[line_count][13])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand1Max
                        if (rcCommand1max < int(csv_reader[line_count][14])) and line_count + 3 < numrow:
                            rcCommand1max = int(csv_reader[line_count][14])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand2Max
                        if (rcCommand2max < int(csv_reader[line_count][15])) and line_count + 3 < numrow:
                            rcCommand2max = int(csv_reader[line_count][15])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand3Max
                        if (rcCommand3max < int(csv_reader[line_count][16])) and line_count + 3 < numrow:
                            rcCommand3max = int(csv_reader[line_count][16])
                line_count += 1

            motor0min = motor0max
            motor1min = motor1max
            motor2min = motor2max
            motor3min = motor3max
            rcCommand0min = rcCommand0max
            rcCommand1min = rcCommand1max
            rcCommand2min = rcCommand2max
            rcCommand3min = rcCommand3max

            line_count = 0
            for row in csv_reader:
                if line_count > 1 and line_count < numrow:     # Finding Motor0Min
                        if (motor0min > int(csv_reader[line_count][38])) and line_count + 3 < numrow:
                            motor0min = int(csv_reader[line_count][38])
                if line_count > 1 and line_count < numrow:     # Finding Motor1Min
                        if (motor1min > int(csv_reader[line_count][39])) and line_count + 3 < numrow:
                            motor1min = int(csv_reader[line_count][39])
                if line_count > 1 and line_count < numrow:     # Finding Motor2Min
                        if (motor2min > int(csv_reader[line_count][40])) and line_count + 3 < numrow:
                            motor2min = int(csv_reader[line_count][40])
                if line_count > 1 and line_count < numrow:     # Finding Motor3Min
                        if (motor3min > int(csv_reader[line_count][41])) and line_count + 3 < numrow:
                            motor3min = int(csv_reader[line_count][41])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand0Min
                        if (rcCommand0min > int(csv_reader[line_count][13])) and line_count + 3 < numrow:
                            rcCommand0min = int(csv_reader[line_count][13])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand1Min
                        if (rcCommand1min > int(csv_reader[line_count][14])) and line_count + 3 < numrow:
                            rcCommand1min = int(csv_reader[line_count][14])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand2Min
                        if (rcCommand2min > int(csv_reader[line_count][15])) and line_count + 3 < numrow:
                            rcCommand2min = int(csv_reader[line_count][15])
                if line_count > 1 and line_count < numrow:     # Finding rcCommand3Min
                        if (rcCommand3min > int(csv_reader[line_count][16])) and line_count + 3 < numrow:
                            rcCommand3min = int(csv_reader[line_count][16])
                line_count +=1
            motor0range = motor0max - motor0min
            motor1range = motor1max - motor1min
            motor2range = motor2max - motor2min
            motor3range = motor3max - motor3min
            rcCommand0range = rcCommand0max - rcCommand0min
            rcCommand1range = rcCommand1max - rcCommand1min
            rcCommand2range = rcCommand2max - rcCommand2min
            rcCommand3range = rcCommand3max - rcCommand3min
            rcCommand0center = 1500
            rcCommand1center = 1500
            rcCommand2center = 1500
            rcCommand3center = 1500

            print(motor0max)
            print(motor1max)
            print(motor2max)
            print(motor3max)
            print(motor0min)
            print(motor1min)
            print(motor1min)
            print(motor1min)
            print("RC Rates")
            print(rcCommand0min)
            print(rcCommand0max)
            print(rcCommand1min)
            print(rcCommand1max)
            print(rcCommand2min)
            print(rcCommand2max)
            print(rcCommand3min)
            print(rcCommand3max)

            line_count = 0
            for row in csv_reader:
                if (line_count % 10000) == 0:  # Simple progress indication
                    print('\r' "Calculation progress: " + str(round((float(line_count / numrow * 100)), 2)) + " %",
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

                    # csv_reader[line_count][32] = "Throttle %"               # Throttle in %"""

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
                    csv_reader[line_count].insert(numcolumn + 8, "0.0")  # Initial Gforece max set to 0
                    csv_reader[line_count].insert(numcolumn + 9, "0.0")  # Initial Motor Power max set to 0
                    csv_reader[line_count].insert(numcolumn + 10, "0.0")  # Initial current draw max set to 0
                    csv_reader[line_count].insert(numcolumn + 11, csv_reader[line_count][
                        numcolumn + 1])  # Initial current Voltage max set to start
                    csv_reader[line_count][38] = round(((float(csv_reader[line_count][38]) - motor0min ) /
                                                        motor0range)*100,1) # Bring Motor load 0 in range 0 - 100%
                    csv_reader[line_count][39] = round(((float(csv_reader[line_count][39]) - motor1min) /
                                                    motor1range)*100, 1)  # Bring Motor load 1 in range 0 - 100%
                    csv_reader[line_count][40] = round(((float(csv_reader[line_count][40]) - motor2min) /
                                                        motor2range)*100, 1)  # Bring Motor load 2 in range 0 - 100%
                    csv_reader[line_count][41] = round(((float(csv_reader[line_count][41]) - motor3min) /
                                                        motor3range)*100, 1)  # Bring Motor load 3 in range 0 - 100%
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
                        ((float(csv_reader[line_count][16]) - 1500 ) / 5),
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
                    csv_reader[line_count][38] = round(((float(csv_reader[line_count][38]) - motor0min) / motor0range)*100,
                                                       1)  # Bring Motor load 0 in range 0 - 100%
                    csv_reader[line_count][39] = round(((float(csv_reader[line_count][39]) - motor1min) /
                                                    motor1range)*100, 1)  # Bring Motor load 1 in range 0 - 100%
                    csv_reader[line_count][40] = round(((float(csv_reader[line_count][40]) - motor2min) /
                                                        motor2range)*100, 1)  # Bring Motor load 2 in range 0 - 100%
                    csv_reader[line_count][41] = round(((float(csv_reader[line_count][41]) - motor3min) /
                                                        motor3range)*100, 1)  # Bring Motor load 3 in range 0 - 100%
                    """csv_reader[line_count][13] = round(
                        ((float(csv_reader[line_count][13]) - rcCommand0min) / rcCommand0range) * 100,
                        1)  # Bring rcCommand 0 in range 0 - 100%
                    csv_reader[line_count][14] = round(
                        ((float(csv_reader[line_count][14]) - rcCommand1min) / rcCommand1range) * 100,
                        1)  # Bring rcCommand 1 in range 0 - 100%
                    csv_reader[line_count][15] = round(
                        ((float(csv_reader[line_count][15]) - rcCommand2min) / rcCommand2range) * 100,
                        1)  # Bring rcCommand 2 in range 0 - 100%
                    csv_reader[line_count][16] = round(
                        ((float(csv_reader[line_count][16]) - rcCommand3min) / rcCommand3range) * 100,
                        1)  # Bring rcCommand 3 in range 0 - 100%"""
                    csv_reader[line_count][13] = round(
                        ((float(csv_reader[line_count][13])) / 5),
                         1)  # Bring rcCommand 0 in range 0 - 100%
                    csv_reader[line_count][14] = round(
                        ((float(csv_reader[line_count][14])) / 5),
                         1)  # Bring rcCommand 1 in range 0 - 100%
                    csv_reader[line_count][15] = round(
                        ((float(csv_reader[line_count][15]) ) / 5),
                         1)  # Bring rcCommand 2 in range 0 - 100%
                    csv_reader[line_count][16] = round(
                        (((float(csv_reader[line_count][16])) - 1500) / 5),
                         1)  # Bring rcCommand 3 in range 0 - 100%

                if (line_count >= 1000) and (line_count < (numrow - 1000)):
                    ave = 0.0

                    for x in range((line_count - 100), line_count):
                        ave = ave + csv_reader[x][numcolumn + 3]
                    ave = round(float(ave / 100.0), 2)
                    csv_reader[line_count - 10].insert(numcolumn + 12, ave)
                line_count += 1


        line_count = 0
        with open('{0}_converted.csv'.format(currentfile[:-4]),
                  mode='w') as output_file:  # add _converted to output filename
            output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if (line_count % 10000) == 0:  # Simple progress indication
                    print('\r' "Write to file progress: " + str(round((float(line_count / numrow * 100)), 2)) + " %",
                          end="")
                output_file.writerow(csv_reader[line_count])
                line_count += 1
        print("Converting of the CSV file successful")
    b += 1
