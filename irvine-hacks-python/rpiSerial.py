import serial

def sendCommand(command):
    ser = serial.Serial("/dev/ttyS0", 9600)
    print(f"Sending {command}")
    ser.write(command)