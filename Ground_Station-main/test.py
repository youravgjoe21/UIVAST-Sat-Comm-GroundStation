import Iridium

rb = Iridium.Iridium()

com = ""

while com != "exit":
    com = input("Input Command: ")
    if com == "sq":
        print(rb.sq())
    elif com == "read":
        print(rb.read())
    elif com == "receive":
        print(rb.receive())
    elif com == "check signal":
        print(rb.check_signal_status())
    elif com == "check message":
        print(rb.check_messages())
    elif com == "send":
        msg = input("Input message: ")
        rb.send(msg)
    elif com == "write":
        msg = input("Input message: ")
        rb.write(msg)
    else:
        print("Invalid command. Valid commands are,\nexit\nsq\nread\nreceive\ncheck signal\ncheck message\nsend\nwrite")

