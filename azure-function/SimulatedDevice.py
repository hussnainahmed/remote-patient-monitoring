# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
from random import randint, random, uniform
# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=rpm-pbi-iothub.azure-devices.net;DeviceId=rpm-pbi-dev-1;SharedAccessKey=TT6is2kJcponO5OSkgzhbsWIWifXLWcIpfTZY4y277M="

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"recorded_at": {recorded_at},"temperature": {temperature},"oxygen_saturation": {oxygen_saturation}, "heart_rate": {heart_rate},"bp_systolic": {bp_systolic},"bp_diastolic": {bp_diastolic}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            #dateTimeObj = datetime.now()
            #timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%S")
            temperature = uniform(36, 37)
            oxygen_saturation = randint(95, 99)
            heart_rate = randint(90, 150)
            bp_systolic = randint(110, 120)
            bp_diastolic = randint(70, 80)
            #humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT.format(
                recorded_at = time.time(),
                temperature=temperature, 
                oxygen_saturation = oxygen_saturation,
                heart_rate = heart_rate,
                bp_systolic = bp_systolic,
                bp_diastolic = bp_diastolic
                )
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            #if temperature > 30:
            #  message.custom_properties["temperatureAlert"] = "true"
            #else:
            #  message.custom_properties["temperatureAlert"] = "false"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(10)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()