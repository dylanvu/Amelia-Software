import serial

def sendCommand(command):
    ser = serial.Serial("/dev/ttyS0", 9600)
    ser.write(command)