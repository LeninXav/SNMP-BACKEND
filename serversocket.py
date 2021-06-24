import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def trap(sid, data):
    print('message ', data)
    sio.emit('trap_event', data)

@sio.event
def trap3(sid, data):
    print('message ', data)
    sio.emit('trap3_event', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)



if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 1000)), app)