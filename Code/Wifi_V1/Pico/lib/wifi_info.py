import time
import socket
import network

ssid = "ATT-WIFI-Yr72"
password = 'iY7r72c7'
server_ip = '0.0.0.0'
port = 12345
server = socket.socket()

def wifi_connect():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    print('Attempting To Connect.')
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        
        time.sleep(1)

    if wlan.status() == 3:
        print('Connected to Wifi')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0])
        return True
    else:
        #raise RuntimeError('Network Connection Failed')
        print('Network Connection Failed')
        return False 
        
def connectSocket(machineID = "Test ID"):
    global server
    try:
        server = socket.socket()
        server.connect((server_ip, port))
        return sendToServer(machineID)
        return True
    except:
        print('Failed To Connect to Server: OFFLINE MODE')
        return False
    
#function to send a message to the server
def sendToServer(msg):
    try:
        server.sendall(bytearray(msg, 'utf-8'))
        return True
    except:
        return False
      
