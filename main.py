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
    if filenames[b][-3:] == "TXT" or filenames[b][-3:] == "bbl":      # Check for  if last 3 digits of each
                                        # list items with filenames machtes
                                        # a betaflight log
        currentfile = filenames[b]
        print("Logfile file found, try to convert  " + currentfile)
        bbdecode = str(pathlib.Path(__file__).parent.absolute()) + "/blackbox_decode --limits --unit-frame-time s " \
                                                               "--unit-height m --unit-rotation deg/s " \
                                                               "--unit-acceleration g --unit-gps-speed kph " \
                                                               "--merge-gps --declination-dec 7.03 " \
                                                               "--unit-vbat V --debug " + filenames[b]  # Start Blackbox decode
                                        # with parameters
        os.system(bbdecode)             # Call blackbox_decode
        print(" Blackbox converted successful to csv ")
    b += 1   # check next file

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
            csv_reader = list(csv.reader(csv_file, delimiter=','))   # import csv file and create list of csv lines
            numcolumn = len(csv_reader[0])                          # determine columns in csv file
            line_count = 0
            for row in csv_reader:                  # Split up GPS coordinates for each
                if line_count == 0:                 # Prepare header row
                    #print(csv_reader[0])
                    csv_reader[line_count].insert(numcolumn + 1, "Time of video (s)")       # Insert Time of video
                    csv_reader[line_count].insert(numcolumn + 2, "Vbat (V)")        # Insert GPS Latitude
                    csv_reader[line_count].insert(numcolumn + 3, "Acceleration total (g)")  # Insert Acceleration
                    csv_reader[line_count].insert(numcolumn + 4, "Total Motor Power (VA)")  # Insert Motor power
                    csv_reader[line_count].insert(numcolumn + 5, "GPS dist home (m)")  # Insert GPS dist home
                    csv_reader[line_count].insert(numcolumn + 6, "GPS dist trav (m)")  # Insert GPS distance traveled home
                    """
                    
                    
                    csv_reader[line_count][32] = "Throttle %"               # Throttle in %"""

                if line_count == 1:
                    csv_reader[line_count].insert(numcolumn + 1, float(0.0))  # Time calculation
                    csv_reader[line_count].insert(numcolumn + 2, float(csv_reader[line_count][21]) / float(10.0))  # Volatge correction
                    csv_reader[line_count].insert(numcolumn + 3, round(math.sqrt(float(csv_reader[line_count][31]) *
                                                                         float(csv_reader[line_count][31]) +
                                                                         float(csv_reader[line_count][32]) *
                                                                         float(csv_reader[line_count][32]) +
                                                                         float(csv_reader[line_count][33]) *
                                                                         float(csv_reader[line_count][33])), 2))  # Calculate acceleration
                    csv_reader[line_count].insert(numcolumn + 4, round(float(csv_reader[line_count][numcolumn + 2]) *
                                                                       float(csv_reader[line_count][22]), 2)) # Calculate Motor power
                    csv_reader[line_count].insert(numcolumn + 5, "0.0")  # Initial Home distance set to 0
                    csv_reader[line_count].insert(numcolumn + 6, "0.0")  # Initial travel distance set to 0
                    csv_reader[line_count][49] = csv_reader[25][49]   # Copy of a later GPS position to use at home.
                    csv_reader[line_count][50] = csv_reader[25][50]  # Copy of a later GPS position to use at home.
                    """
                    csv_reader[line_count][32] = round(float(float(csv_reader[line_count][32])
                                                             + 1024.0)/20.48, 2)  # convert throttle to %"""

                if line_count >= 2:
                    csv_reader[line_count].insert(numcolumn + 1, (round(float(csv_reader[line_count][1]) - float(csv_reader[line_count-1][1]) + float(csv_reader[line_count-1][numcolumn]), 5)))  # Time calc.
                    csv_reader[line_count].insert(numcolumn + 2, round(float(csv_reader[line_count][21]) / float(10.0), 2))  # Volatge correction
                    csv_reader[line_count].insert(numcolumn + 3, round(math.sqrt(float(csv_reader[line_count][31]) *
                                                                           float(csv_reader[line_count][31]) +
                                                                           float(csv_reader[line_count][32]) *
                                                                           float(csv_reader[line_count][32]) +
                                                                           float(csv_reader[line_count][33]) *
                                                                           float(csv_reader[line_count][
                                                                                     33])), 2))  # Calculate acceleration
                    csv_reader[line_count].insert(numcolumn + 4, round(float(csv_reader[line_count][numcolumn + 1]) *
                                                                      float(csv_reader[line_count][22]), 2)) # Calculate Motor power

                    csv_reader[line_count].insert(numcolumn + 5, round((haversine(float(csv_reader[20][49]),
                                                                float(csv_reader[20][50]),
                                                                float(csv_reader[line_count - 1][49]),
                                                                float(csv_reader[line_count - 1][50]))), 2)
                                                  )  # Calculating distance to home using the GPS coordinate form line 20 as the home point
                    csv_reader[line_count].insert(numcolumn + 6, round((float(haversine(float(csv_reader[line_count][49]),
                                                                      float(csv_reader[line_count][50]),
                                                                      float(csv_reader[line_count - 1][49]),
                                                                      float(csv_reader[line_count - 1][50]))) +
                                                  float(csv_reader[line_count - 1][numcolumn + 5])), 2)
                                                  )  # Using the GPS coordinate to caclculate distance traveled
                    """csv_reader[line_count][32] = round(float(
                        float(csv_reader[line_count][32]) + 1024.0) / 20.48,2)  # convert Throttle to %"""
                line_count += 1

        line_count = 0
        with open('{0}_converted.csv'.format(currentfile[:-4]), mode='w') as output_file:       # add _converted to output filename
                output_file = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in csv_reader:
                    output_file.writerow(csv_reader[line_count])
                    line_count += 1
        print("Converting of the CSV file successful")
    b += 1
