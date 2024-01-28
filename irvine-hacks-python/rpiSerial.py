import serial

def sendCommand(command):
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    print(f"Sending {command}")
    # convert the string to bytes
    commandBytes = command.encode('utf-8')
    ser.write(commandBytes)