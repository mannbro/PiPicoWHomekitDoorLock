import config
import network
import socket
from utime import sleep_ms
from uselect import select
from machine import Pin

    
#Set up pins
RELAY_PIN=16

#Pulse length in ms
PULSE_LENGTH=500

#States
TARGET_LOCK_STATE_UNSECURED=0
TARGET_LOCK_STATE_SECURED=1

CURRENT_LOCK_STATE_UNSECURED = 0
CURRENT_LOCK_STATE_SECURED = 1
CURRENT_LOCK_STATE_JAMMED = 2
CURRENT_LOCK_STATE_UNKNOWN = 3


#Setup pins for relay and sensors
relay = Pin(RELAY_PIN, Pin.OUT)
wifi = network.WLAN(network.STA_IF)

#Global statuses
targetState=TARGET_LOCK_STATE_SECURED
currentState=CURRENT_LOCK_STATE_SECURED

def connectWifi():
    global wlan

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(config.ssid, config.password)

    max_wait = 10
    while wifi.status() != 3:
        print('waiting for connection. Status: '+str(wifi.status()))
        sleep_ms(1000)

    print('connected')
    status = wifi.ifconfig()
    ipAddress=status[0]
    print( 'ip = ' + ipAddress )

connectWifi()

#Set up socket and start listening on port 80
addr = socket.getaddrinfo(wifi.ifconfig()[0], 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)

def unlockDoor():
    print('unlockDoor')
    setTargetState(TARGET_LOCK_STATE_UNSECURED)
#    setCurrentState(CURRENT_LOCK_STATE_UNSECURED)
    relay.value(1)
    sleep_ms(PULSE_LENGTH)
    relay.value(0)

    retval=getLockStates()

    setTargetState(TARGET_LOCK_STATE_SECURED)
    setCurrentState(CURRENT_LOCK_STATE_SECURED)

    return retval

def lockDoor():  
    print('lockDoor')
    setTargetState(TARGET_LOCK_STATE_SECURED)
    setCurrentState(CURRENT_LOCK_STATE_SECURED)
    return getLockStates()

def returnError(errcode):
    return '{"success": false, "error": "'+errcode+'"}'

def getLockStates():
    print('getLockStates')
    global targetState
    global currentState

    return '{"success": true, "currentState": '+str(currentState)+', "targetState": '+str(targetState)+'}'

def setTargetState(state):
    global targetState
    
    if(state==TARGET_LOCK_STATE_UNSECURED):
        targetState=TARGET_LOCK_STATE_UNSECURED
    else:
        targetState=TARGET_LOCK_STATE_SECURED
    
def setCurrentState(state):
    global currentState
    
    if(state==CURRENT_LOCK_STATE_UNSECURED):
        currentState=CURRENT_LOCK_STATE_UNSECURED
    else:
        currentState=CURRENT_LOCK_STATE_SECURED

#Handle an incoming request
def handleRequest(conn, address):
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)

    print(request)

    if request.find('/?unlock')==6:
        response=unlockDoor()
    elif request.find('/?lock')==6:
        response=lockDoor()
    elif request.find('/?getstatus')==6:
        response=getLockStates()
    else:
        response=returnError('UNKNOWN_COMMAND')

    print(response)

    conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
    conn.send(response)
    conn.close()

#Main Loop
while True:
    #Check if wifi is connected, if not, reconnect
    if wifi.isconnected() == False:
        print('Connecting wifi...')
        connectWifi()

    #Handle incoming HTTP requests in a non-blocking way
    r, w, err = select((s,), (), (), 1)

    #Is there an incoming request? If so, handle the request
    if r:
        for readable in r:
            conn, addr = s.accept()
            try:
                handleRequest(conn, addr)
            except OSError as e:
                pass
