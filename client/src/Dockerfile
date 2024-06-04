# Use uma imagem base do Node.js
FROM node:18-buster as build

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de configuração do npm 
COPY package.json ./

# Instale as dependências do npm e pnpm
RUN npm install -g pnpm concurrently
RUN pnpm install

# Copie todo o código do projeto para o contêiner
COPY . .

# Instale as dependências do Python e libGL
RUN apt-get update && apt-get install -y python3-pip libgl1

# Execute o comando de inicialização
CMD ["npm", "run", "start"]
