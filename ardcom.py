import warnings
import serial
import serial.tools.list_ports
import time
from datetime import datetime
import re
import os
import logging

tries = 50
def find_arduino(serial_number):
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            return serial.Serial(pinfo.device, baudrate=115200, timeout=.1)
    logging.critical("Could not find an arduino - is it plugged in?")
    input("arduino nenalezeno")
    os._exit(0)
arduino = find_arduino(serial_number='A9H5X9N6A')
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.02)
    data = arduino.readline()
    return data
def get_formatted_datetime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
    return formatted_datetime
def compare_strings(string1, string2):
    pattern = re.compile(string2)
    match = re.search(pattern, string1)
 
    if match:
        logging.info(f"'{string2}' found in '{string1}'")
        return True
    else:
        logging.info(f"'{string2}' not found in '{string1}'")
        return False
try:
    for i in range(tries):
        result = get_formatted_datetime()
        logging.info(result)
        value = write_read(result)
        logging.info(value)
        value = str(value)
        for i in range(6):
            data = arduino.readline()
            logging.info(data)
        if compare_strings(value, result):
            logging.warning("datum nahrano")
            input("Datum nahrano...")
            os._exit(0)   
    logging.error("datum nebylo uspesne nahrano")
    input("datum nebylo uspesne nahrano")
except exception as e:
    logging.critical(e)
    input("Press enter to exit")
    os._exit(0)