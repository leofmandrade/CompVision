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




def process(filename):
    data = pd.read_excel(filename)
    kills = data['KILLS'].tolist()
    data['KILLS'] = kills
    data.to_excel(filename, index=False)

    deaths = data['DEATHS'].tolist()
    data['DEATHS'] = deaths
    data.to_excel(filename, index=False)

    assists = data['ASSISTS'].tolist()
    data['ASSISTS'] = assists
    data.to_excel(filename, index=False)

    champions = data['CHAMPION'].tolist()
    champion = max(set(champions), key=champions.count)

    for i in range(1, len(champions)):
        if champions[i] != champion:
            champions[i] = champion

    data['CHAMPION'] = champions
    data.to_excel(filename, index=False)

    farm = data['FARM'].tolist()
    data['FARM'] = farm
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

    

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    print (data)
    youtubeURL = data['imageUrl']
    if not youtubeURL:
        return jsonify({'error': 'YouTube URL is required'}), 400

    try:
        video = YouTube(youtubeURL)
        video_stream = video.streams.filter(file_extension='mp4', adaptive=True, only_video=True).order_by('resolution').desc().first()
        if video_stream:
            video_stream.download(output_path='videos', filename='video.mp4')    
            return jsonify({'message': 'Video downloaded successfully'})
        else:
            return jsonify({'error': 'No video stream found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



FILE_NAMES = [
    'dados_1.0.xlsx', 'dados_2.0.xlsx', 'dados_3.0.xlsx', 'dados_4.0.xlsx',
    'dados_5.0.xlsx', 'dados_6.0.xlsx', 'dados_7.0.xlsx', 'dados_8.0.xlsx',
    'dados_9.0.xlsx', 'dados_10.0.xlsx', 'dados_BLUE.xlsx', 'dados_RED.xlsx', 
]

FILES_DIRECTORY = os.getcwd()

@app.route('/download', methods=['GET'])
def download_files():
    print ('download')
    
    # /code
    output_folder = 'frames'
    if os.path.exists(output_folder):
        files = os.listdir(output_folder)
        for file in files:
            file_path = os.path.join(output_folder, file)
            os.remove(file_path)
    video_path = 'videos/video.mp4'
    interval_seconds = 50
    capture_frames(video_path, output_folder, interval_seconds)
    print ('frames captured')


    # /csv
    folder = 'frames'
    pathicons = 'championIcons'

    i = 3000
    csvData = []

    while True:
        filename = f"frame_{i}.jpg"
        full_path = os.path.join(folder, filename)
        full_path = full_path.replace('\\', '/')
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


    # /data
    data = pd.read_csv('data.csv')
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
        nome_arquivo_jogador = f'dados_{jogador}.xlsx'
        jogadorData.to_excel(nome_arquivo_jogador, index=False)



    # /process
    all_data = pd.DataFrame()
    for i in range(1, 11):
        filename = f'dados_{i}.0.xlsx'
        data = pd.read_excel(filename)
        process(filename)
        all_data = pd.concat([all_data, data], ignore_index=True)
    all_data.to_excel('dados_todosPlayers.xlsx', index=False)
    dataBlue = pd.read_excel('dados_BLUE.xlsx')
    dataRed = pd.read_excel('dados_RED.xlsx')
    dataBlue = dataBlue[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataRed = dataRed[['TIME', 'GOLD', 'TOWERS', 'DRAGONS', 'ARAUTO', 'LARVA', 'KILLS', 'frame']]
    dataBlue = process_tophud(dataBlue)
    dataRed = process_tophud(dataRed)
    dataBlue.to_excel('dados_BLUE.xlsx', index=False)
    dataRed.to_excel('dados_RED.xlsx', index=False)


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


@app.route('/eachChampData', methods=['GET'])
def eachChampData():
    jsonChampions = {}
    for i in range(1, 11):
        filename = f'dados_{i}.0.xlsx'
        data = pd.read_excel(filename)
        jsonChampions[f'champ{i}'] = data.to_dict(orient='records')
        print (f'champ{i}: {data.to_dict(orient="records")}')
    return jsonify(jsonChampions)


@app.route('/results', methods=['GET'])
def results():
    jsonChampions = {}
    for i in range(1, 11):
        filename = f'dados_{i}.0.xlsx'
        data = pd.read_excel(filename)
        champions = data['CHAMPION'].tolist()
        jsonChampions[f'champ{i}'] = champions[0]
        print (f'champ{i}: {champions[0]}')
    return jsonify(jsonChampions)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)