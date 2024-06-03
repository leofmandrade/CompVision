# Use uma imagem base que contém Python e todas as dependências necessárias
FROM python:3.11-slim


# Instale dependências de sistema necessárias
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Crie um diretório de trabalho
WORKDIR /app

# Copie os arquivos do seu projeto para o diretório de trabalho
COPY . /app

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o servidor Flask
CMD ["python", "server.py"]
