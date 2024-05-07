from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

    # const handleImageChange = (event) => {
    #     const file = event.target.files[0];
    #     if (file && file.type.substr(0, 5) === "image") {
    #         setImage(URL.createObjectURL(file));
    #         fetch ('http://localhost:8080/api', {
    #             method: 'POST',
    #             body: file
    #         })
    #     } else {
    #         setImage(null);
    #     }
    # };
@app.route('/api', methods=['GET'])
# def api que recebe o body e retorna true se for uma imagem:
def api():
    file = request.files['file']
    if file and file.mimetype.startswith('image'):
        return jsonify({'valid': True})
    return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(debug=True, port=8080)