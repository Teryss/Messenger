import socket
import threading as t

PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!D'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER)

rooms = {}
nicknames = []

def create_room(conn, name, username):
    for key in rooms.keys():
        if key == name:
            return
    rooms[name] = [[conn, username]]
    response = f'Room {name} has been created'.encode(FORMAT)
    conn.sendall(response)

def send_msg_room(name, username, msg):
    response = f'[{username}] {msg}'.encode(FORMAT)
    for conn, room_user in rooms[name]:
        if room_user != username:
            conn.sendall(response)
        else:
            print(conn,room_user)

def join_room(conn, name, username):
    for roomName, data in rooms.items():
        if roomName == name:
            for i in range(len(data)):
                if data[i][1] == username:
                    username += '(1)'
            rooms[roomName].append([conn,username])
            send_msg_room(roomName, 'SERVER', f'{username} joined a room!')
            break

def handleClient(conn, addr):
    print(f"[CONNECTED] {addr}")
    connected = True
    while connected:
        try:
            stream = conn.recv(1024).decode(FORMAT)
            if stream:
                print(f'{addr} : {stream}')
                #CREATING A ROOM
                if stream[0] == 'C':
                    sstream = stream.split(';')
                    room_name = sstream[1]
                    username = sstream[2]
                    create_room(conn, room_name, username)

                #HANDLE SENDING MESSAGES TO USERS IN A ROOM
                if stream[0] == 'T':
                    sstream = stream.split(';')
                    room = sstream[1]
                    username = sstream[2]
                    msg = sstream[3]
                    send_msg_room(room, username, msg)

                #JOIN A USER TO A ROOM
                if stream[0] == 'J':
                    sstream = stream.split(';')
                    room = sstream[1]
                    username = sstream[2]
                    join_room(conn, room, username)

                #DISCONNECT A USER
                if stream[0] == DISCONNECT_MSG:
                    connected = False
        except:
            print(f"Unexpected disconnection! Connection from {addr} has been closed!")
            connected = False
    conn.close()
    print(f"[DISCONNECTED] {addr}")

def run():
    server.listen()
    print(f"[SERVER INFO] Listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()
        thread = t.Thread(target=handleClient, args=(conn, addr))
        print(f"Connections count: {t.active_count() - 1}")
        thread.start()

if __name__ == "__main__":
    print("[START] SERVER IS STARING")
    run()