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


file_path = 'eeg_data.csv'
csv_file = open(file_path, mode='a', newline='', buffering=1)  # Open file in append mode with line buffering
csv_writer = csv.writer(csv_file)


# Configuration
ip = '0.0.0.0'
port = 5000

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


    Args:
        address (str): The OSC address from which data is received.
        *args: Variable arguments which include EEG data values.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Include milliseconds
    row = [timestamp] + list(args)
    csv_writer.writerow(row)  # Write data row to the CSV file


def sensor_handler(address, *args):
    print(f"Received {address}: {args}")

def battery_handler(address, *args):
    print(f"Received {address}: {args}")

def gyro_handler(address, *args):
    print(f"Received {address}: {args}")

def acc_handler(address, *args):
    print(f"Received {address}: {args}")

def blink_handler(address, *args):
    print(f"Received {address}: {args}")

def jaw_clench_handler(address, *args):
    print(f"Received {address}: {args}")

def marker_handler(address, *args):
    print(f"Received {address}: {args}")

def setup_dispatcher():
    disp = dispatcher.Dispatcher()
    disp.map("/muse/eeg", eeg_handler)


   
    
    return disp

async def main():
    disp = setup_dispatcher()
    server = osc_server.AsyncIOOSCUDPServer((ip, port), disp, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Creates the endpoint and starts serving
    print(f"Serving on {ip}:{port}")

    await asyncio.Future()  # This keeps the server running indefinitely

if __name__ == "__main__":
    asyncio.run(main())



# disp.map("/muse/elements/delta_absolute", brainwave_handler)
# disp.map("/muse/elements/theta_absolute", brainwave_handler)
# disp.map("/muse/elements/alpha_absolute", brainwave_handler)
# disp.map("/muse/elements/beta_absolute", brainwave_handler)
# disp.map("/muse/elements/gamma_absolute", brainwave_handler)
#disp.map("/Marker/*", marker_handler)

# disp.map("/muse/elements/horseshoe", sensor_handler)
# disp.map("/muse/elements/touching_forehead", sensor_handler)
# disp.map("/muse/batt", battery_handler)
# disp.map("/muse/gyro", gyro_handler)
# disp.map("/muse/acc", acc_handler)
# disp.map("/muse/elements/blink", blink_handler)
# disp.map("/muse/elements/jaw_clench", jaw_clench_handler)