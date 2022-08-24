import socket
import threading

SERVER_IP = '192.168.56.1'
PORT = 5050
SERVER = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!D'
CREATEROOM_MSG = 'C'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER)

def createRoom(name, username):
    stream = f'C;{name};{username}'.encode(FORMAT)
    client.send(stream)

def joinRoom(name, username):
    stream = f'J;{name};{username}'.encode(FORMAT)
    client.send(stream)
    print(f"Joined {name}")

def send(room, username):
    run = True
    print(f"To disconnect from {room} enter {DISCONNECT_MSG}")
    while run:
        if threading.active_count() < 3:
            break
        try:
            msg = input("")
            if msg == DISCONNECT_MSG:
                stream = DISCONNECT_MSG
                run = False
            else:
                stream = ';'.join(('T', room, username, msg))
            stream = stream.encode(FORMAT)
            client.send(stream)
        except:
            client.close()
            print("Something broke while sending")
            break

def receive_msg():
    while True:
        if threading.active_count() < 3:
            break
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
        except:
            client.close()
            print("Something broke while receiving")
            break
def run():
    sending_thread = threading.Thread(target=send, args=(room_name, username))
    sending_thread.start()
    receiving_thread = threading.Thread(target=receive_msg)
    receiving_thread.start()
a = input("Do you want to join a room or create one? j/c: ")

if a.lower() == 'c':
    info = input("Enter room name and username (ex. my_room;fred): ").split(';')
    room_name = info[0]
    username = info[1]
    createRoom(room_name, username)
    msg = client.recv(1024).decode(FORMAT)
    run()
elif a.lower() == 'j':
    info = input("Enter room name and username (ex. my_room;fred): ").split(';')
    room_name = info[0]
    username = info[1]
    joinRoom(room_name, username)
    run()