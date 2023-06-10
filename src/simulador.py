import zmq, time, threading

UMIDADE = 29

class ServerSimulador(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global UMIDADE
        print("Iniciando o simulador")
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        while True:
            message = socket.recv()
            socket.send(str(UMIDADE).encode())

class ThreadSimulador(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global UMIDADE

        while True:
            time.sleep(5)
            UMIDADE -= 0.5
    
def main():
    simulador = ThreadSimulador("ambiente")
    servidor = ServerSimulador("servidor-web")

    simulador.start()
    servidor.start()

main()
