from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import random



app = Flask(__name__)
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, resources={r"/*": {"origins": "*"}})

values = {
    'slider1': 25,
    'slider2': 0,
}
conexoes=0

@app.route('/')
def index():
    return render_template('index.html',**values)

@socketio.on('connect')
def test_connect(data):
    global conexoes 
    conexoes = conexoes +1
    print('connect= alguem conectou ')
    print(data)
    emit('after connect',  {'data':'Conexoes '+str(conexoes)})

# EVENTO #1 Slider value changed
@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(values)


@socketio.on('comando_executar')
def evento_executado(payload='vazio'):   
    #print(payload)
    print('entrou no evento executado #1....')
    print(random.randint(0, 50))
    
    payload['who']='slider'+str(random.randint(1,2))
    payload['data']=random.randint(0, 50)
    print(payload)
    emit('executado',  payload)
    #values=values['slider1'] = random.randint(0, 50)
    emit('update value', payload, broadcast=True)
    print('entrou no evento executado #2....')


if __name__ == '__main__':
    socketio.run(app,port=8081, host='0.0.0.0')