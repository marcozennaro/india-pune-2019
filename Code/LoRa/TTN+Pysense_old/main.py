from network import LoRa
import binascii
import struct
from lib.MPL3115A2 import MPL3115A2
from lib.LTR329ALS01 import LTR329ALS01
from lib.SI7006A20 import SI7006A20
from lib.LIS2HH12 import LIS2HH12
import socket
import time
import pycom
from pysense import Pysense


lora = LoRa(mode=LoRa.LORAWAN)

dev_addr = struct.unpack(">l", binascii.unhexlify('26011984'))[0]
nwk_swkey = binascii.unhexlify('5ECF005491EC779608B81BDD50D90C1D')
app_swkey = binascii.unhexlify('462175A1109541A7AF1342374F3628D7')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

py = Pysense()
tempHum = SI7006A20(py)

while True:
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    s.setblocking(False)
    # Read data from the libraries and place into string
    temperature = tempHum.temp()
    humidity = tempHum.humidity()
    print("Temperature: {} Degrees  Humidity: {}".format(temperature, humidity))

    data = "%.2f %.2f " % (tempHum.temp(), tempHum.humidity())
    #multi.temp(), lux.lux()[0], multi.humidity(), accel.roll(), accel.pitch(), accel.yaw())
    print("Sending %s" % data)
    # send the data over LPWAN network
    s.send(data)
    s.settimeout(3.0) # configure a timeout value of 3 seconds
    try:
       rx_pkt = s.recv(64)   # get the packet received (if any)
       print(rx_pkt)
    except socket.timeout:
      print('No packet received')
