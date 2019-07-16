from network import LoRa
import binascii
import struct

lora = LoRa(mode=LoRa.LORAWAN)

dev_addr = struct.unpack(">l", binascii.unhexlify('260118A2'))[0]
nwk_swkey = binascii.unhexlify('F913FB6F4E47169234163839D5A76787')
app_swkey = binascii.unhexlify('CB4DECE3104D7B5EB85AFFD8334E45E3')

lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

import socket
import time

while True:
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

    s.setblocking(False)
    s.send(bytes([1, 2, 3]))
    s.settimeout(3.0) # configure a timeout value of 3 seconds
    try:
       rx_pkt = s.recv(64)   # get the packet received (if any)
       print(rx_pkt)
    except socket.timeout:
      print('No packet received')
