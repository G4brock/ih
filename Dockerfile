FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /IH

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências usando o gerenciador de pacotes pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do projeto para o diretório de trabalho
COPY . .

# Comando de execução padrão quando o contêiner for iniciado
CMD python3 src/simulador.py & python3 src/sensor.py & python3 src/atuador.py & python3 src/main.py
