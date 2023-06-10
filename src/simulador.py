import zmq, time, threading

UMIDADE = 29
VARIACAOTEMP = -0.5

class ServerSimulador(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global UMIDADE, VARIACAOTEMP
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        while True:
            message = socket.recv()
            message = str(message).split("'")[1]

            if(message == "getTemperatura"):
                socket.send(str(UMIDADE).encode())
            elif(message == "setTemperatura/pos"):
                VARIACAOTEMP = -0.5
                socket.send("Atuador desativado".encode())
            elif(message == "setTemperatura/neg"):
                VARIACAOTEMP = 0.5
                socket.send(f"Atuador ativado".encode())


class ThreadSimulador(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global UMIDADE, VARIACAOTEMP

        while True:
            time.sleep(1)
            UMIDADE += VARIACAOTEMP
    
    
def main():
    simulador = ThreadSimulador("ambiente")
    servidor = ServerSimulador("servidor-web")

    simulador.start()
    servidor.start()

    print("Simulador Iniciado")


main()
