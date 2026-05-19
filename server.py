import socket
import threading
import os

port = int(os.environ.get("PORT", 5555))
host = '0.0.0.0'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    # අයින් වුණු අය ඉවත් කරලා ඉතිරි අයට විතරක් ආරක්ෂිතව මැසේජ් යවනවා
    for client in clients[:]: 
        try:
            client.send(message)
        except:
            # මැසේජ් එක යවන්න බැරි නම් ඒ client ව අයින් කරනවා
            try:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
            except:
                pass

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise Exception()
            broadcast(message)
        except:
            try:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                broadcast(f"⚠️ [SYSTEM]: {nickname} left the chat!".encode('utf-8'))
            except:
                pass
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            nicknames.append(nickname)
            clients.append(client)
            
            broadcast(f"🟢 [SYSTEM]: {nickname} joined the chat!".encode('utf-8'))
            
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            pass

print(f"🎮 Server is running on port {port}...")
receive()