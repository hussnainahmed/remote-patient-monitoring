"""
Read data from a BerryMed pulse oximeter, model BM1000C, BM1000E, etc.
"""

# Protocol defined here:
#     https://github.com/zh2x/BCI_Protocol
# Thanks as well to:
#     https://github.com/ehborisov/BerryMed-Pulse-Oximeter-tool
#     https://github.com/ScheindorfHyenetics/berrymedBluetoothOxymeter
#
# The sensor updates the readings at 100Hz.

import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_berrymed_pulse_oximeter import BerryMedPulseOximeterService
from time import sleep
import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import adafruit_requests as requests
from adafruit_azureiot import IoTCentralDevice

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# With a Particle Argon
RX = board.ESP_TX
TX = board.ESP_RX
resetpin = DigitalInOut(board.ESP_WIFI_EN)
rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
esp_boot.direction = Direction.OUTPUT
esp_boot.value = True


print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=False
)

URL = "http://wifitest.adafruit.com/testwifi/index.html"
print("ESP AT GET URL", URL)

print("Resetting ESP module")
esp.hard_reset()

requests.set_socket(socket, esp)

#JSON_POST_URL = 'https://shifa-rpm.streamfunctions.io/api/v1/862BV4P65kAaR90LlD18/telemetry'




# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

pulse_ox_connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(Advertisement, timeout=5):
        name = adv.complete_name
        if not name:
            continue
        # "BerryMed" devices may have trailing nulls on their name.
        if name.strip("\x00") == "BerryMed":
            pulse_ox_connection = ble.connect(adv)
            print("Connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")

    try:
        print("Checking connection...")
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        if pulse_ox_connection and pulse_ox_connection.connected:
            print("Fetch connection")
            device = IoTCentralDevice(socket,esp,secrets["id_scope"],secrets["device_id"],secrets["key"])
            device.connect()
            if DeviceInfoService in pulse_ox_connection:
                dis = pulse_ox_connection[DeviceInfoService]
                try:
                    manufacturer = dis.manufacturer
                except AttributeError:
                    manufacturer = "(Manufacturer Not specified)"
                try:
                    model_number = dis.model_number
                except AttributeError:
                    model_number = "(Model number not specified)"
                print("Device:", manufacturer, model_number)
            else:
                print("No device information")
            pulse_ox_service = pulse_ox_connection[BerryMedPulseOximeterService]
            count= 99;
            while pulse_ox_connection.connected:
                count = count + 1;
                values = pulse_ox_service.values
                if count % 100 != 0:
                    continue;
                else:
                    try:
                        if values.valid and values.spo2 <= 100:
                            if values.spo2 == 100:
                                spo2 = 99
                            else:
                                spo2 = values.spo2
                            #print(spo2)
                            #key_to_lookup = 'spo2'
                            #if key_to_lookup in values:
                            message = {"spo2": spo2,"pulse_rate": values.pulse_rate}
                            print(message)
                            start = time.monotonic()
                            device.send_telemetry(json.dumps(message))
                            device.loop()
                            #response = requests.post(JSON_POST_URL, json=json_data)
                            #json_resp = response.content
                            print(time.monotonic()- start)
                            #print(json_resp)
                            print("-" * 40)
                    except Exception as e:
                        print(str(e))
                        #print(pulse_ox_service.values)
                        #print(time.monotonic())
                #sleep(5)
    except _bleio.ConnectionError:  # pylint: disable=no-member
        try:
            pulse_ox_connection.disconnect()
        except _bleio.ConnectionError:  # pylint: disable=no-member
            pass
        pulse_ox_connection = None