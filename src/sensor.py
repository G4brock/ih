import zmq, threading, time

CONTEXT  = zmq.Context()
TEMPERATURA = 0

class GetData(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global TEMPERATURA, CONTEXT

        socket = CONTEXT.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        while True:
            time.sleep(10)
            print("Analisando Temperatura...")
            socket.send("Hello".encode())
            msg = socket.recv();

            TEMPERATURA = str(msg).split("'")[1]
            print(f"Temperatura atual: {TEMPERATURA} °C")
            
        

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
            socket.send(str(TEMPERATURA).encode())


def main():
    get = GetData("getSensor1")
    send = SendData("sendSensor1")

    send.start()
    get.start()

main()
