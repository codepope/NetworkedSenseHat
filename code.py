import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
# import adafruit_requests as requests
# import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol
import board
import busio
import adafruit_lps2x
import adafruit_hts221
import adafruit_lsm9ds1
import json

SERVERIP="192.168.111.199"
SERVERPORT=8080

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

TX = board.GP0
RX = board.GP1
#resetpin = DigitalInOut(board.ESP_WIFI_EN)
#rtspin = DigitalInOut(board.ESP_CTS)
uart = busio.UART(TX, RX, timeout=0.1)
# esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
# esp_boot.direction = Direction.OUTPUT
# esp_boot.value = True
lps25h_addr = 0x5c
lsm9ds1_mag_addr = 0x1c
hts221_addr = 0x5f # Matches Adafruit breakout and library - here for reference
led2472g_addr = 0x46
lsm9ds1_xg_addr = 0x6a

i2c=busio.I2C(board.GP21,board.GP20)
lps25h=adafruit_lps2x.LPS25(i2c,lps25h_addr)
hts221=adafruit_hts221.HTS221(i2c)
lsm9ds1=adafruit_lsm9ds1.LSM9DS1_I2C(i2c,lsm9ds1_mag_addr,lsm9ds1_xg_addr)

esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, debug=False
    # , reset_pin=resetpin, rts_pin=rtspin,
)

while True:
    try:
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        status={}
        status["lps25h"]={ "pressure":lps25h.pressure, "temperature":lps25h.temperature}
        status["hts221"]={ "relhumidity":hts221.relative_humidity, "temperature": hts221.temperature}
        accel_x, accel_y, accel_z = lsm9ds1.acceleration
        mag_x, mag_y, mag_z = lsm9ds1.magnetic
        gyro_x, gyro_y, gyro_z = lsm9ds1.gyro
        temp = lsm9ds1.temperature

        status["lsm9ds1"]={ "accel": { "x":accel_x, "y":accel_y, "z":accel_z}, 
                    "mag": { "x":mag_x,"y":mag_y,"z":mag_z},
                    "gyro": { "x":gyro_x, "y":gyro_y, "z":gyro_z},
                    "temperature": temp}

        socket=esp.socket_connect(esp.TYPE_TCP, SERVERIP, SERVERPORT, keepalive=10, retries=1)
        buffer=bytes(json.dumps(status),'utf-8')
        pream=bytes(f'POST / HTTP/1.1\nContent-Type: text/plain\nHost: {SERVERIP}\nContent-Length: {len(buffer)}\n\n','utf-8')
        esp.socket_send(pream+buffer,1)
        resp=esp.socket_receive(10)
        print(resp.decode('utf-8'))
        esp.socket_disconnect()
        print("Sent update")
        time.sleep(10)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to send data, retrying\n", e)
        print("Resetting ESP module")
        esp.hard_reset()
        continue


