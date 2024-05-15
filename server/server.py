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
