import serial
import serial.tools.list_ports
import warnings
import csv
from StringIO import StringIO
import time
import re

ser = []

def arduinoPort(baud):
    for p in serial.tools.list_ports.comports():
        if p.description in ('Arduino','Generic CDC'):
            #print p
            ser.append(p.device)

    if not ser:
        raise IOError("No Arduino found")
    if len(ser) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
        #print ser[0]
    return serial.Serial(ser[0], baud)

class sensor_stats:

    def __init__(self, temperature, light, timestamp):
        self.temperature = temperature
        self.light = light
        self.time = timestamp

def is_number(string):
    """
    Given a string returns True if the string represents a number.
    Returns False otherwise.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def clean_serial_data(data):
    """
    Given a list of serial lines (data). Removes all characters.
    Returns the cleaned list of lists of digits.
    Given something like: ['0.5000,33\r\n', '1.0000,283\r\n']
    Returns: [[0.5,33.0], [1.0,283.0]]
    """
    clean_data = [time.time()]

    for line in data:
        line_data = re.findall("\d*\.\d*|\d*",line) # Find all digits
        line_data = [float(element) for element in line_data if is_number(element)] # Convert strings to float
        if len(line_data) >= 2:
            clean_data.append(line_data)
    save_to_csv(clean_data, 'tank_stats.csv')
    return clean_data

def save_to_csv(data, filename):
    """
    Saves a list of lists (data) to filename
    """
    with open(filename, 'a') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerows(data)
