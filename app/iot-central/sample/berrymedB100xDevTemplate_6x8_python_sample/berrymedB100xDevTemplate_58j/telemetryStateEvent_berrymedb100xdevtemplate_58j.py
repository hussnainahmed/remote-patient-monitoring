# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

# berrymedB100xDevTemplate_6x8_python_sample/@berrymedB100xDevTemplate_58j/telemetryEventState.py

import json

def CreateBlob():
  return {
    'spo2': 1, # <- try another value!
    'pulse_rate': 2, # <- try another value!
  }

def Send(device):
  device.sendTelemetry(json.dumps(CreateBlob()))
