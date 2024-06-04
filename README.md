# League of Legends Data


## Feito por Arthur Fonseca, Caio Tieri e Leonardo Andrade

Este é um projeto de aplicativo que extrai dados das imagens de uma partida de League of Legends a partir de um vídeo do YouTube. Ele utiliza computação visual para processar os dados dos jogadores ao longo do tempo e disponibiliza um arquivo Excel com os dados coletados.

Devido ao alto consumo de memória do código, não foi possível fazer o deploy em um site de hospedagem gratuito. Foram feitos inúmeros testes com diversas configurações e em diversos sites gratuitos (Vercel, Railway, Render...), mas todos apresentaram problemas de consumo de memória ou de tempo de execução na hora de rodar o servidor. Por isso, a única forma que foi encontrada é utilizar o aplicativo é baixando o repositório e rodando localmente.



## Instruções de Uso

1. Clone o repositório em sua máquina local:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Navegue até o diretório do cliente:

```bash
cd nome-do-repositorio/client/src
```

3. Instale as dependências do Python:

```bash
pip install -r requirements.txt
```

4. Instale as dependências do Node.js:

```bash
npm install
```

5. Inicie o servidor local:

```bash
npm run dev
```

6. Abra o navegador e acesse `http://localhost:3000` para utilizar o aplicativo.

7. Na página inicial, insira o link do vídeo do YouTube contendo a partida de League of Legends e clique em "Run".

8. Após a extração dos dados, surgirá um novo botão "Process Results". Clique nele para exportar os dados para um arquivo Excel e ir para a página dos gráficos.

## Funcionalidades

- **Extrair Dados**: Insira o link do vídeo do YouTube contendo a partida de League of Legends e o aplicativo irá processar as imagens para extrair os dados dos jogadores ao longo do tempo por meio de gráficos.	
  
- **Exportar para Excel**: O aplicativo permite exportar os dados coletados para um arquivo Excel para análise posterior.

- **OBS**: A extração de todos os dados realmente leva muito tempo, então é necessário aguardar um pouco, se quiser, da pra acompanhar o progresso no console do navegador pelo que o servidor está fazendo.

- **OBS2**: O aplicativo foi, inicialmente, desenvolvido para que o jogador colocasse um intervalo de tempo que ele quisesse que os dados fossem extraídos. Entretando, devido a muitos problemas com a extração de dados com alguns intervalos de tempo durante a fase de testes do aplicativo, chegamos em um tempo ótimo de 50 segundos entre cada frame, que é o utilizado atualmente.

- **OBS3**: Os dados extraídos não são 100% precisos, mas são bem próximos do real, então não leve os dados como verdade absoluta. Alguns fatores como a qualidade do vídeo, a resolução, a quantidade de frames por segundo, a quantidade de jogadores na tela, a quantidade de texto na tela, entre outros, influenciam na precisão dos dados extraídos.

- **OBS4**: O aplicativo foi desenvolvido durante o patch 14.09 e 14.10 com o server NA, então os dados extraídos são baseados nesse patch e nesse server, então fique por conta e risco se for utilizar os dados extraídos para análises de outros patches ou servers, não é garantido que os dados serão precisos.

- **OBS5**: Os testes para este aplicativo foram conduzidos utilizando replays de partidas de League of Legends disponibilizados pelo canal [ChallengerReplays](https://www.youtube.com/@ChallengerReplays) do YouTube. Utilizamos os vídeos desse canal como fonte de dados para verificar a eficácia e precisão das funcionalidades de extração de dados do nosso aplicativo. Essa fonte nos permitiu realizar testes extensivos e garantir a qualidade do sistema de processamento de imagens.




## Tecnologias Utilizadas

- **React**: Utilizado para a construção da interface do usuário.
  
- **Next.js**: Framework React utilizado para renderização do lado do servidor e geração de páginas estáticas.

- **OpenCV**: Biblioteca de visão computacional utilizada para processar as imagens e extrair os dados dos jogadores.

- **EasyOCR**: Biblioteca de OCR (Reconhecimento Óptico de Caracteres) utilizada para reconhecer os textos nas imagens.



## Créditos
Todos os direitos autorais do design, estilo e elementos visuais do jogo pertencem à Riot Games, Inc. Este projeto é feito por fãs e não tem afiliação oficial com a Riot Games, Inc.

Alguns elementos visuais utilizados neste aplicativo foram inspirados no jogo League of Legends e são utilizados aqui de acordo com a política de uso de conteúdo de fãs da Riot Games, Inc. Para mais informações sobre o uso de conteúdo de fãs, consulte [este link](https://www.riotgames.com/en/legal).

League of Legends é uma marca registrada da Riot Games, Inc.
