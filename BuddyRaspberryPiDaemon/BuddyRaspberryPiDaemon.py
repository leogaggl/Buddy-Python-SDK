import sys
import time
from curses_check_for_keypress import CheckForKeypress

# TODO: Make sure you are using the correct GPIO package.

# The following import is used by the fakeRPiGPIO package, for testing outside of Raspberry Pi.
# import RPi.GPIO as GPIO

# The following import is used by the RPi.GPIO package, for testing on a Raspberry Pi.
from RPi import GPIO


GPIO.VERBOSE = False

GPIO.setmode(GPIO.BCM)

channel_list = [4]

GPIO.setup(channel_list, GPIO.IN, GPIO.PUD_DOWN)

sys.path.append("../Buddy Python SDK")
sys.path.append("../Buddy Python SDK/buddysdk")

from buddysdk import buddy

# TODO: Go to http://dev.buddyplatform.com to get an app ID and app key.
buddy.init("<Your App ID>", "<Your App Key>")

# A PUT must be done to configure your app's telemetry. See https://dev.buddyplatform.com/docs/IoT%20Telemetry#ConfigureTelemetry for more details.
buddy.put("/telemetry/RaspberryPi", {})

c = CheckForKeypress('Buddy Raspberry Pi SDK Sample', test_mode=True)

while c.input() is None:

    outputs = [GPIO.input(channel) for channel in channel_list]

    data = {"pins": dict(zip(channel_list, outputs))}

    print "GPIO status: " + str(data) + "\r"

    response = buddy.post("/telemetry/RaspberryPi", {"data": data})

    print "Telemetry response: " + str(response) + "\r"

    time.sleep(2)

GPIO.cleanup(channel_list)

c.cleanup()
