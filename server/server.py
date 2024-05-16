from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from pytube import YouTube
import pandas as pd
import cv2
import os
import funcs as f
import zipfile


app = Flask(__name__)
CORS(app)

def capture_frames(video_path, output_folder, interval_seconds):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({'error': 'Error opening video'})

    #take screenshots every interval_seconds of the video and save it in a folder /frames
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % (interval_seconds * 30) == 0:
            cv2.imwrite(f'{output_folder}/frame_{frame_count}.jpg', frame)
            print (f'Frame {frame_count} captured')
            print (f'Frame capture in {output_folder}/frame_{frame_count}.jpg')
        frame_count += 1

    cap.release()
    return jsonify({'message': 'Frames captured successfully'})



def getDataFromFrames():
    print ('pegadno dados dos frames')
    folder = 'frames'
    pathicons = 'championIcons'

    i = 3000
    csvData = []

    while True:
        filename = f"frame_{i}.jpg"
        full_path = os.path.join(folder, filename)
        full_path = full_path.replace('\\', '/')
        print (full_path)

        if os.path.isfile(full_path):
            print (full_path, "exists")
            df, df2 = f.run(full_path, pathicons)
           

            df['frame'] = i
            df2['frame'] = i


            csvData.append(df.to_dict(orient='records'))
            csvData.append(df2.to_dict(orient='records'))
            i += 1500
            print (i)

        else:
            print (full_path, "does not exist")
            break
    
    print (csvData)
    concatData = [item for sublist in csvData for item in sublist]
    csv = pd.DataFrame(concatData)
    csv.to_csv('data.csv', index=False)            

    return jsonify({'message': 'Data extracted successfully'})

def process_kills(filename):
    data = pd.read_excel(filename)
    kills = data['KILLS'].tolist()

    for i in range(1, len(kills)):
        # se for menor que o anterior ou for igual a "erro", substituir pelo anterior
        print (f'File: {filename}')

        if kills[i] == 'S':
            print (f'mudou de S para 5')
            kills[i] = '5'

        if kills[i] == 'erro':
            print (f'mudou de erro pro valor antigo')
            kills[i] = kills[i-1]

        if int(kills[i]) < int(kills[i-1]):
            print (f'File: {filename}')
            print (type(kills[i]), type(kills[i-1]))
            print (f'Kills: {kills[i]} < Kills: {kills[i-1]}')
            print (f'-----------------')
            kills[i] = kills[i-1]
            print (f'AGORA KILLS: {kills[i]}')
    data['KILLS'] = kills
    data.to_excel(filename, index=False)

def process_deaths(filename):
    data = pd.read_excel(filename)
    deaths = data['DEATHS'].tolist()

    for i in range(1, len(deaths)):
        # se for menor que o anterior ou for igual a "erro", substituir pelo anterior
        # print (f'File: {filename}')
        # print ("deaths atual", deaths[i], "deaths anterior", deaths[i-1])
        # se for a e o anterior for 3, substituir por 4
        # se for a e o anterior for 4, substituir por 4
        if (deaths[i] == 'a' and deaths[i-1] == '3') or (deaths[i] == 'a' and deaths[i-1] == '4'):
            # print (f'mudou de a para 4')
            deaths[i] = '4'

        if deaths[i] == 'S':
            # print (f'mudou de S para 5')
            deaths[i] = '5'

        if deaths[i] == 'erro':
            # print (f'mudou de erro pro valor antigo')
            deaths[i] = deaths[i-1]

    for i in range(1, len(deaths)):
        # se o de agora for maior que o anterior, e menor que o proximo, substituir pelo anterior
        if (int(deaths[i]) > int(deaths[i-1])) and (int(deaths[i]) > int(deaths[i+1])):
            print (f'File: {filename}')
            print (type(deaths[i]), type(deaths[i-1]))
            print (f'Deaths: {deaths[i]} > Deaths: {deaths[i-1]} < Deaths: {deaths[i+1]}')
            print (f'-----------------')
            deaths[i] = deaths[i-1]
            print (f'AGORA Deaths: {deaths[i]}')
        # se o de agora for menor que o anterior
        if (int(deaths[i]) < int(deaths[i-1])):
            print (f'File: {filename}')
            print (type(deaths[i]), type(deaths[i-1]))
            print (f'Deaths: {deaths[i]} < Deaths: {deaths[i-1]}')
            print (f'-----------------')
            deaths[i] = deaths[i-1]
            print (f'AGORA Deaths: {deaths[i]}')

    data['DEATHS'] = deaths
    data.to_excel(filename, index=False)

def process_assists(filename):
    data = pd.read_excel(filename)
    assists = data['ASSISTS'].tolist()

    for i in range(1, len(assists)):
        # se for menor que o anterior ou for igual a "erro", substituir pelo anterior
        print (f'File: {filename}')

        if assists[i] == 'S':
            print (f'mudou de S para 5')
            assists[i] = '5'

        if assists[i] == 'erro':
            print (f'mudou de erro pro valor antigo')
            assists[i] = assists[i-1]

        if int(assists[i]) < int(assists[i-1]):
            print (f'File: {filename}')
            print (type(assists[i]), type(assists[i-1]))
            print (f'Assists: {assists[i]} < Assists: {assists[i-1]}')
            print (f'-----------------')
            assists[i] = assists[i-1]
            print (f'AGORA Assists: {assists[i]}')
    data['ASSISTS'] = assists
    data.to_excel(filename, index=False)

def process_champions(filename):
    data = pd.read_excel(filename)

    # roda a coluna CHAMPION e ve qual o campeao com mais ocorrencias. trocar tudo que for diferente dele, por ele
    champions = data['CHAMPION'].tolist()
    champion = max(set(champions), key=champions.count)

    for i in range(1, len(champions)):
        # se for diferente do campeao mais escolhido, substituir pelo campeao mais escolhido
        if champions[i] != champion:
            champions[i] = champion
            print(f'Campeao trocado para {champion}')

    data['CHAMPION'] = champions
    data.to_excel(filename, index=False)


def process_tophud(dataframe):
    colunas = dataframe.columns
    for coluna in colunas:
        for i in range(1, len(dataframe[coluna])):
            if coluna == 'GOLD':
                if len(dataframe[coluna][i]) ==3:
                    dataframe[coluna][i] = dataframe[coluna][i][0] + dataframe[coluna][i][1] +  "." + dataframe[coluna][i][2]
            if dataframe[coluna][i] == 'No text detected':
                dataframe[coluna][i] = dataframe[coluna][i-1]
    return dataframe


@app.route('/process', methods=['GET'])
def process():

    all_data = pd.DataFrame()
    for i in range(1, 11):
        filename = f'dados_{i}.0.xlsx'
        data = pd.read_excel(filename)
        process_champions(filename)
        print ('=================')
        process_kills(filename)
        print ('=================')
        process_deaths(filename)
        print ('=================')
        process_assists(filename)
        print ('=================')

        all_data = pd.concat([all_data, data], ignore_index=True)
        # print (data)

    all_data.to_excel('dados_todosPlayers.xlsx', index=False)

 

    dataBlue = pd.read_excel('dados_BLUE.xlsx')
    dataRed = pd.read_excel('dados_RED.xlsx')
    # deixar somente as colunas que interessam e salvar ele de volta no arquivo
    # TIME	GOLD	TOWERS	DRAGONS	ARAUTO	LARVA	KILLS	frame
    dataBlue = dataBlue[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataRed = dataRed[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataBlue = process_tophud(dataBlue)
    dataRed = process_tophud(dataRed)
    dataBlue.to_excel('dados_BLUE.xlsx', index=False)
    dataRed.to_excel('dados_RED.xlsx', index=False)

    process_kills('dados_BLUE.xlsx')
    process_kills('dados_RED.xlsx')
    return jsonify({'message': 'Data extracted successfully'})

@app.route('/data', methods=['GET'])
def data():
# Ler o CSV
    data = pd.read_csv('data.csv')

    # Agrupar os dados com base na coluna 'TIME'
    grupos = data.groupby('TIME')

    # Salvar cada grupo em um arquivo Excel separado
    for time, grupo in grupos:
        nome_arquivo = f'dados_{time}.xlsx'  # Nome do arquivo baseado no tempo de jogo
        grupo.to_excel(nome_arquivo, index=False)


    jogadores = data['PLAYER'].unique()

    for jogador in jogadores:
        jogadorData = data[data['PLAYER'] == jogador]
        jogadorData = jogadorData[['KILLS', 'frame', 'PLAYER', 'TEAM', 'DEATHS', 'ASSISTS', 'FARM', 'CHAMPION']]

        
        print (jogadorData)
        print ('-----------------')
        print (jogador)

        # Salvar os dados do jogador em um arquivo Excel com o nome do jogador
        nome_arquivo_jogador = f'dados_{jogador}.xlsx'
        jogadorData.to_excel(nome_arquivo_jogador, index=False)



    return jsonify({'message': 'Data extracted successfully'})

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    print (data)
    youtubeURL = data['imageUrl']
    if not youtubeURL:
        return jsonify({'error': 'YouTube URL is required'}), 400

    try:
        video = YouTube(youtubeURL)
        video_stream = video.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
        video_stream.download(output_path='videos', filename='video.mp4')    
        return jsonify({'message': 'Video downloaded successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/code', methods=['GET'])
def code():
    # do the code of capturing frames with the video path, output folder and interval seconds
    video_path = 'videos/video.mp4'
    output_folder = 'frames'
    interval_seconds = 50
    return capture_frames(video_path, output_folder, interval_seconds)



@app.route('/csv', methods=['GET'])
def csv():
    # do the function getDataFromFrames() to get the data from the frames
    print ('Getting data from frames')
    return getDataFromFrames()


FILE_NAMES = [
    'dados_1.0.xlsx', 'dados_2.0.xlsx', 'dados_3.0.xlsx', 'dados_4.0.xlsx',
    'dados_5.0.xlsx', 'dados_6.0.xlsx', 'dados_7.0.xlsx', 'dados_8.0.xlsx',
    'dados_9.0.xlsx', 'dados_10.0.xlsx', 'dados_BLUE.xlsx', 'dados_RED.xlsx', 'dados_todosPlayers.xlsx'
]

FILES_DIRECTORY = os.getcwd()

@app.route('/download', methods=['GET'])
def download_files():
    try:
        zip_filename = "dados_files.zip"
        zip_filepath = os.path.join(FILES_DIRECTORY, zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for file_name in FILE_NAMES:
                file_path = os.path.join(FILES_DIRECTORY, file_name)
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
        
        return send_file(zip_filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True, port=8080)
