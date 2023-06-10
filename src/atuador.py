import zmq, threading, time

CONTEXT  = zmq.Context()
TEMPERATURA = 0
SERVER_ID = ["id-0001"]

            
class SendData(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global TEMPERATURA, CONTEXT, SERVER_ID
        
        replier = CONTEXT.socket(zmq.REP)
        replier.bind("tcp://*:5553")

        request = CONTEXT.socket(zmq.REQ)
        request.connect("tcp://localhost:5555")

        while True:
            message = replier.recv()
            message = str(message).split("'")[1].split("/")
            if(message[1] in SERVER_ID):
                if(message[2] == "setTemperatura"):
                    request.send(f"{message[2]}/{message[3]}".encode())
                    message = request.recv()
                    replier.send(message)
                else:
                    replier.send("Ação inválida".encode())
            else:
                replier.send("Servidor não identificado, retorno bloqueado.")


def main():
    send = SendData("sendSensor1")

    send.start()

    print("Atuador Funcionando")

main()
