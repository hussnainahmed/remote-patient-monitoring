# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

# berrymedB100xDevTemplate_6x8_python_sample/main.py

import datetime
import sys
import connection

sys.path.append('berrymedB100xDevTemplate_58j') # search in berrymedB100xDevTemplate_58j interface
import telemetryStateEvent_berrymedb100xdevtemplate_58j as berrymedB100xDevTemplate_58j_telemetry

# want to connect another device? just update the credentials below
SCOPE_ID = '0ne0015FAF2'
DEVICE_ID = 'dpincvesxvl5gtnyp5kfip'
KEY = 'P5binluUpcq0NjDKJ1mdZ4nySUZPwIRegXxEdbTKLfg='

gCounter = 0
gDevice = None

def callback(info): # iotc.IOTCallbackInfo
  global gDevice

  if gDevice == None:
    gDevice = info.getClient()

  if info.getEventName() == 'ConnectionStatus':
    if info.getStatusCode() == 0:
      if gDevice.isConnected():
        print(str(datetime.datetime.now()), 'Connected!')
        return
    print(str(datetime.datetime.now()), 'Connection Lost?')
    gDevice = None
    return

  if info.getEventName() == 'SettingsUpdated':
    print(str(datetime.datetime.now()), 'Received an update to device settings.')
# there was no device settings definition for the device

  if info.getEventName() == 'Command':
    print(str(datetime.datetime.now()), 'Received a C2D from cloud to device settings.')
# there was no C2D (cloud to device) definition for the device

def main():
  global gCounter, gDevice

  while True:
    gDevice = connection.Connect(SCOPE_ID, DEVICE_ID, KEY, callback)

    while gDevice != None and gDevice.isConnected():
      gDevice.doNext() # do the async work needed to be done for MQTT
      if gCounter % 10 == 0: # every 10 seconds
        gCounter = 0

        # sending telemetry for berrymedB100xDevTemplate_58j interface
        print(str(datetime.datetime.now()), 'sending telemetry for berrymedB100xDevTemplate_58j interface')
        berrymedB100xDevTemplate_58j_telemetry.Send(gDevice)

      gCounter += 1

main()
