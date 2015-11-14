import RPIO
import select
import sys

import Buddy


print('Buddy Raspberry Pi SDK Sample')

Buddy.init("bbbbbc.xgjbvPdwkllw", "1E9E824E-A3F1-4F34-B4F4-9CC87471A564")

# A PUT must be done to configure your app's telemetry. See https://dev.buddyplatform.com/docs/IoT%20Telemetry#ConfigureTelemetry for more details.
Buddy.put("/telemetry/RaspberryPi", {})



while True:

	i, o, e = select.select( [sys.stdin], [], [], 5 )


	options = {
		"data" : { "value_a" : 1, "value_b" : True },
		"location" : "47.1, -121.292"
	}


	Buddy.post("/telemetry/RaspberryPi", options)


	if (i):
		break

