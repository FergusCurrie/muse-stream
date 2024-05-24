"""
OSC implementation to read from muse headset. 

OSC = open sound control. Similar to json/xml. Is a format for waveform data. 
peer-peer messaing protocol 
message = address + data 

looks kinda like rest api

pythonosc
- osc_server
    - AsyncIOOCUDPServer
- dispatcher
    - Dispatcher

"""

from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import csv 
from datetime import datetime
from dotenv import load_dotenv
import os 

load_dotenv()

# BASE_DIR will be set in production as env variable 
BASE_DIR = os.environ.get('BASE_DIR')
if not BASE_DIR:
    BASE_DIR = "test_data/"



# Configuration
IP = '0.0.0.0'
PORT = 5000

# headers 
EEG_HEADER = "timestamp, tp9, af7, af8, tp10, auxR, auxL"
ABSOLUTE_POWER_BAND_HEADER = "timestamp, type, value"
ACCELEROMETER_HEADER = "timestamp, x, y, z"
GYRO_HEADER = "timestamp, x, y, z"
HORSESHOE_HEADER = "timestamp, s1, s2, s3, s4"
BATTERY_HEADER = "timestamp, state_of_charge, fuel_gauge_battery_voltage, adc_battery_voltage, temperature"

def open_writer(path):
    return csv.writer(open(path, mode='a', newline='', buffering=1))

# csv writers 
eeg_csv_writer = open_writer(BASE_DIR+os.environ.get('EGG_PATH'))
abs_power_band_csv_writer = open_writer(BASE_DIR+os.environ.get('ABS_POWER_BAND_PATH'))
accelerometer_writer =open_writer(BASE_DIR+os.environ.get('ACCELEROMTER_PATH'))
horseshoe_writer = open_writer(BASE_DIR+os.environ.get('HORSESHOE_PATH')) 
gyro_writer = open_writer(BASE_DIR+os.environ.get('GYRO_PATH')) 
battery_writer = open_writer(BASE_DIR+os.environ.get('BATTERY_PATH')) 

def write_csv(csv_writer, args):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Include milliseconds
    row = [timestamp] + list(args)
    csv_writer.writerow(row)


def eeg_handler(address, *args):
    """
    Handle incoming EEG data and append it to a CSV file.
    delta, gamma etc are just extracted from raw data 
    : 
    - TP9 - Left ear
    - AF7 - Left forehead
    - AF8 - Right forehead
    - TP10 - Right ear
    - AUXR - Right Auxiliary
    - AUXL - Left Auxiliary (MS-01/MS-02 only)

    https://web.archive.org/web/20181105231756/http://developer.choosemuse.com/tools/available-data#Absolute_Band_Powers

    https://en.wikipedia.org/wiki/Neural_oscillation

    https://mind-monitor.com/FAQ.php#oscspec


    Args:
        address (str): The OSC address from which data is received.
        *args: Variable arguments which include EEG data values.
    """
    write_csv(eeg_csv_writer, args)

def absolute_power_band_handler(address, *args):
    """
    Receive abs band powers delta, theta, alpha, beta, gamma and store to csv. 
    Data comes in at 10hz.

    """
    args = list(args)
    args = [address.split('/')[-1]] + args
    write_csv(abs_power_band_csv_writer, args)

def accelerometer_handler(address, *args):
    """
    Receive x,y,z gravity and store to csv. 
    Data comes in at 50.

    """
    write_csv(accelerometer_writer, args)

def gyro_handler(address, *args):
    """
    Receive x,y,z and store to csv. 
    Data comes in at 50.

    """
    write_csv(gyro_writer, args)

def test_handler(address, *args):
    print(f"Received {address}: {args}")

def battery_handler(address, *args):
    """
    [State of charge, Fuel gauge battery voltage, ADC battery voltage, Temperature]
    """
    write_csv(battery_writer, args)

def horseshoe_handler(address, *args):
    write_csv(horseshoe_writer, args)

def setup_dispatcher():
    disp = dispatcher.Dispatcher()
    disp.map("/muse/eeg", eeg_handler)
    disp.map("/muse/acc", accelerometer_handler)
    disp.map("/muse/elements/delta_absolute", absolute_power_band_handler)
    disp.map("/muse/elements/theta_absolute", absolute_power_band_handler)
    disp.map("/muse/elements/alpha_absolute", absolute_power_band_handler)
    disp.map("/muse/elements/beta_absolute", absolute_power_band_handler)
    disp.map("/muse/elements/gamma_absolute", absolute_power_band_handler)
    disp.map("/muse/elements/horseshoe", horseshoe_handler)
    disp.map("/muse/gyro", gyro_handler)
    disp.map("/muse/batt", battery_handler)
    return disp

async def main():
    disp = setup_dispatcher()
    server = osc_server.AsyncIOOSCUDPServer((IP, PORT), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Creates the endpoint and starts serving
    print(f"Serving on {IP}:{PORT}")

    await asyncio.Future()  # This keeps the server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())