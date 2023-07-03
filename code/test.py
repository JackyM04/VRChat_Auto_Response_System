import yaml
import os
import sys
import random
import argparse
import threading
import pyOSC3
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client


parser = argparse.ArgumentParser()
parser.add_argument("--ip",
    default="127.0.0.1", help="The ip to listen on")
parser.add_argument("--port",
    type=int, default=9001, help="The port to listen on")
args = parser.parse_args()
server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
#启动OSclient
parser_c = argparse.ArgumentParser()
parser_c.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser_c.add_argument("--port", type=int, default=9000,
    help="The port the OSC server is listening on")
args_c = parser_c.parse_args()
client = udp_client.SimpleUDPClient(args_c.ip, args_c.port)

def grtt(arg):
    while True:
        data, client_addr = server.socket.recvfrom(server.max_packet_size)
        try:
            dec = pyOSC3.decodeOSC(data)
            print("{},{}".format(arg, dec))
        except:
            pass
'''''
for i in range(1,11):
    t = threading.Thread(target=grtt, args=(i,))
    t.start()
'''
def test(a):
    while True:
        a +=1
        print(a)
        time.sleep(1)

t = threading.Thread(target=test, args=(0,))
t.start()
t = threading.Thread(target=test, args=(0,))
t.start()

length = len(threading.enumerate())
print('当前运行的线程数为：%d'%length)