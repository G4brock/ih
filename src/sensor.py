import zmq, threading, time

CONTEXT  = zmq.Context()
TEMPERATURA = 0
SERVER_ID = ["id-0001"]

class GetData(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global TEMPERATURA, CONTEXT

        socket = CONTEXT.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        while True:
            time.sleep(5)
            socket.send("getTemperatura".encode())
            msg = socket.recv();
            TEMPERATURA = str(msg).split("'")[1]
            

class SendData(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global TEMPERATURA, CONTEXT
        
        socket = CONTEXT.socket(zmq.REP)
        socket.bind("tcp://*:5554")
        while True:
            message = socket.recv()
            message = str(message).split("'")[1].split("/")

            if(message[1] in SERVER_ID):
                if(message[2] == "getTemperatura"):
                    socket.send(str(TEMPERATURA).encode())
                else:
                    socket.send("Ação inválida".encode())
            else:
                socket.send("Servidor não identificado, retorno bloqueado.")


def main():
    get = GetData("getSensor1")
    send = SendData("sendSensor1")

    send.start()
    get.start()

    print("Sensor funcionando.")


main()
