# NetworkedSenseHat

Sends Sense Hat data over wifi via a Pico and ESP01 as a JSON packet

This would have been a server but the Pico CircuitPython lacks socketpool, wifi, ssl and other
libraries making that, currently impossible. Instead, this variant sends a JSON packet with a
HTTP POST method every ten seconds to a pre-selected server.

Conenction to the Sense Hat via Red Robotics Pico To Pi board (I used the +Proto Version).

Assumes ESP01 in on GPIO 0 and GPIO1. Change for other ESP01 connections.

Set the IP address in the code and the port as SERVERIP and SERVERPORT. You have to use IP as
there's no DNS lookup on the Pico currently.

It will be sent a HTTP POST Method with a JSON packet of data for decoding:

```
{
  "lsm9ds1": {
    "temperature": 21.5,
    "accel": { "z": 7.52184, "y": 6.54317, "x": -0.367298 },
    "mag": { "z": -2.43698, "y": 0.2373, "x": 0.41062 },
    "gyro": { "z": 0.0305433, "y": 0.00106901, "x": 0.0873537 }
  },
  "lps25h": { "pressure": 1003.65, "temperature": 27.3104 },
  "hts221": { "temperature": 25.2326, "relhumidity": 49.9132 }
}
```

Requires a secrets.py with wifi SSID and Password, eg:

```
secrets = {
    'ssid' : 'mynetwork',
    'password' : 'mypassword',
}
```

