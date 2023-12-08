
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask import make_response

app = Flask(__name__)


socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*": {"origins": "*"}})

values = {
    'slider1': 25,
    'slider2': 0,
}

#rota html
@app.route('/')
def index():
    # Enable Access-Control-Allow-Origin
    response = make_response(render_template('index.html',**values))

    response.headers.set("Batata", "frita")
    return response

#rota de eventos
@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)

# Notice how socketio.run takes care of app instantiation as well.
if __name__ == '__main__':
    #192.168.1.103
    socketio.run(app,port=5001,host="0.0.0.0",debug=True)