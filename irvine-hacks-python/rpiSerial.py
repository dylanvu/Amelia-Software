
def sendCommand(command, ser):
    print(f"Sending {command}")

    # convert the string to bytes
    # commandBytes = command.encode('utf-8')
    ser.write(bytes(command, "utf-8"))
    # while True:
        # pass
    # print(commandBytes)
    ser.close()

if __name__ == "__main__":
    sendCommand("0")