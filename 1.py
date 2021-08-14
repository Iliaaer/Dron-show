import os
import platform
import threading
import socket
import netifaces
import netaddr
import socket
import requests 
from datetime import datetime

possible_addr = []


def scan_Ip(ip):
    addr = net + str(ip)
    comm = ping_com + addr
    response = os.popen(comm)
    data = response.readlines()
    for line in data:
        if 'TTL' in line:
            print(addr, "--> Ping Ok")
            possible_addr.append(addr)
            break
            

net = netifaces.gateways()['default'][2][0]
print('You IP :',net)
net_split = net.split('.')
a = '.'
net = net_split[0] + a + net_split[1] + a + net_split[2] + a
start_point = 1
end_point = 255
##start_point = int(input("Enter the Starting Number: "))
##end_point = int(input("Enter the Last Number: "))

oc = platform.system()
if (oc == "Windows"):
    ping_com = "ping -n 1 "
else:
    ping_com = "ping -c 1 "

t1 = datetime.now()
print("Scanning in Progress:")
for ip in range(start_point, end_point):
    if ip == int(net_split[3]):
       continue
    potoc = threading.Thread(target=scan_Ip, args=[ip])
    potoc.start()
potoc.join()
t2 = datetime.now()
total = t2 - t1

print("Scanning completed")
detect_Tello_Arduino = {}
for ip in possible_addr:
    url = 'http://' + ip + '/'
    print(url)
    try:
        r = requests.get(url)
        a = r.text.split('<h2>')[1].split('</h2>')[0]
        print(a)
        detect_Tello_Arduino[a] = ip
    except:
        print('No')
        pass

print(detect_Tello_Arduino)

from wifiArduino import *
from time import sleep

led_on(detect_Tello_Arduino['Tello1'])
sleep(1)
led_off(detect_Tello_Arduino['Tello1'])
sleep(1)
led_on(detect_Tello_Arduino['Tello1'])
