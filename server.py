from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from random_word import RandomWords
r = RandomWords()
app = Flask(__name__)
word = ''
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")
id = {}
i =1
palo = 0
round = 0
scores = {}
@app.route('/Game', methods=['POST'])
def Game():
    global i
    # Get the message from the request's JSON data
    data = request.get_json()
    message = data.get('name')
    id[i] = message
    scores[message] = 0
    socketio.emit('lobby_update', scores)
    response = {'status': 'Player joined'}
    i = i+1
    return jsonify(response)
@app.route('/clear', methods=['POST'])
def Clear():
    global i ,palo, id,scores,round
    id ={}
    scores ={}
    i =1
    palo = 0
    round = 0
    response = {'status': 'Server Cleared'}
    print("server Cleared")
    return jsonify(response)
@app.route('/Start', methods=['POST'])
def start():
    global word
    word = r.get_random_word()
    socketio.emit('start',len(word))
    print("stared game")
    return word
@app.route('/Restart', methods=['POST'])
def restart():
    global word
    word = r.get_random_word()
    for player in scores:
        scores[player] = 0
    socketio.emit('lobby_update', scores)
    socketio.emit('start',len(word))
    print("restared game")
    return word
@app.route('/getName', methods=['GET'])
def get_data():
    return jsonify(scores)
@app.route('/letterinfo', methods=['POST'])
def receive_letterinfo():
    global palo
    letterinfo = request.get_json()
    letter = letterinfo['letterinfo'][0]
    playerId = letterinfo['letterinfo'][1]
    indices = find(letter)
    lenth = len(indices)
    name = id[playerId]
    sc = scores[name] 
    sc = sc + lenth*10
    scores[name] = sc
    palo = palo+1
    palo = palo%len(scores)
    response = [letter,indices,palo]
    socketio.emit('lobby_update', scores)
    socketio.emit('arr_update', response)
    return jsonify(response)
def find(letter):
    return [i for i, char in enumerate(word) if char == letter]
if __name__ == '__main__':
    app.run(debug=True)