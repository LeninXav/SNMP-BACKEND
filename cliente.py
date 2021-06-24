import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')



@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:6000')
print("Emit")
sio.emit('my_message', 'Hola')
sio.sleep(2)
sio.disconnect()