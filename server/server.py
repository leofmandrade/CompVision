from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from io import BytesIO
from pytube import YouTube
import pandas as pd
import cv2
import os
import funcs as f


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
    count = 0
    csvData = []

    while True or count < 5:
        count += 1
        filename = f"frame_{i}.jpg"
        full_path = os.path.join(folder, filename)
        full_path = full_path.replace('\\', '/')
        print (full_path)

        if os.path.isfile(full_path):
            print (full_path, "exists")
            df, df2 = f.run(full_path, pathicons)
            print (df)
            print ("-----------------")
            print (df2)

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

  
@app.route('/process', methods=['GET'])
def process():

    for i in range(1, 11):
        filename = f'dados_{i}.0.xlsx'
        data = pd.read_excel(filename)
        process_kills(filename)
        # print (data)

    dataBlue = pd.read_excel('dados_BLUE.xlsx')
    dataRed = pd.read_excel('dados_RED.xlsx')
    # deixar somente as colunas que interessam e salvar ele de volta no arquivo
    # TIME	GOLD	TOWERS	DRAGONS	ARAUTO	LARVA	KILLS	frame
    dataBlue = dataBlue[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataRed = dataRed[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataBlue.to_excel('dados_BLUE.xlsx', index=False)
    dataRed.to_excel('dados_RED.xlsx', index=False)

    process_kills('dados_BLUE.xlsx')
    process_kills('dados_RED.xlsx')

    # print (dataBlue)
    # print ('-----------------')
    # print (dataRed)
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







if __name__ == '__main__':
    app.run(debug=True, port=8080)
