import zmq, threading, time

CONTEXT  = zmq.Context()
ID_SERVER = "id-0001"
TEMP_LIMITE_POS = int(40)
TEMP_LIMITE_NEG = int(16)

class GetData(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global ID_SERVER, CONTEXT, TEMP_LIMITE_POS

        sensor = CONTEXT.socket(zmq.REQ)
        sensor.connect("tcp://localhost:5554")

        atuador = CONTEXT.socket(zmq.REQ)
        atuador.connect("tcp://localhost:5553")

        while True:
            time.sleep(10)
            print("Analisando Sensor de Temperatura...")
            sensor.send(f"server/{ID_SERVER}/getTemperatura".encode())
            msg = sensor.recv();
            
            TEMPERATURA = float(str(msg).split("'")[1])
            print(f"Temperatura atual: {TEMPERATURA} °C")
            if(TEMPERATURA > TEMP_LIMITE_POS):
                atuador.send(f"server/{ID_SERVER}/setTemperatura/pos".encode())
                atuador.recv()
                print("Baixando Temperatura")
            elif(TEMPERATURA < TEMP_LIMITE_NEG):
                atuador.send(f"server/{ID_SERVER}/setTemperatura/neg".encode())
                atuador.recv()
                print("Subindo Temperatura")


def main():
    get = GetData("getSensor1")
 
    get.start()

main()
