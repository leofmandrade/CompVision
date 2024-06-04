# League of Legends Data Extractor

Este é um projeto de aplicativo que extrai dados das imagens de uma partida de League of Legends a partir de um vídeo do YouTube. Ele utiliza computação visual para processar os dados dos jogadores ao longo do tempo e disponibiliza um arquivo Excel com os dados coletados.

Devido ao alto consumo de memória do código, não foi possível fazer o deploy em um site de hospedagem gratuito. Portanto, para executar o aplicativo, siga as instruções abaixo:

## Instruções de Uso

1. Clone o repositório em sua máquina local:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Navegue até o diretório do cliente:

```bash
cd nome-do-repositorio/client/src
```

3. Instale as dependências:

```bash
npm install
```

4. Inicie o servidor local:

```bash
npm run dev
```

5. Abra o navegador e acesse `http://localhost:3000` para utilizar o aplicativo.

## Funcionalidades

- **Extrair Dados**: Insira o link do vídeo do YouTube contendo a partida de League of Legends e o aplicativo irá processar as imagens para extrair os dados dos jogadores ao longo do tempo.
  
- **Exportar para Excel**: O aplicativo permite exportar os dados coletados para um arquivo Excel para análise posterior.

## Tecnologias Utilizadas

- **React**: Utilizado para a construção da interface do usuário.
  
- **Next.js**: Framework React utilizado para renderização do lado do servidor e geração de páginas estáticas.

- **OpenCV**: Biblioteca de visão computacional utilizada para processar as imagens e extrair os dados dos jogadores.

- **Excel.js**: Biblioteca para geração de arquivos Excel a partir dos dados coletados.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue se encontrar algum problema ou sugerir melhorias.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).