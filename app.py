from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*": {"origins": "*"}})

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html',**values)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(values)

if __name__ == '__main__':
    socketio.run(app,port=8081, host='0.0.0.0')