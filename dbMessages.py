from flask import Flask, session, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'quicktutor'
socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')

@socketio.on('message')
def broadcastMessage(msg):
    # print('Message: ' + msg)
    #send(msg, broadcast=True)
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
        {'data': message['data'], 'count': session['receive_count']}, broadcast=True)

    # for sending a msg to just the room I believe its the code below
    # emit('my_response',
    #  {'data': message['data'], 'count': session['receive_count']},
    #     room=message['room'])

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

if __name__ == '__main__':
    socketio.run(app, debug=True)
