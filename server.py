from threading import Thread
import socket
 

def main():
    HOST = "localhost"
    PORT = 5678

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.bind((HOST, PORT))
    sock.listen(100)

    print("Server is up!")

    clients = {}
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(True)

            nick = conn.recv(1024).decode()
            clients[conn] = nick

            user_joined(conn, clients)
            # не смог без потоков
            Thread(target=client_thread, args=(conn, addr, clients)).start()
        except Exception as e:
                continue
    
# на каждого юзера создаем поток. Ждем сообщения бродкастим
def client_thread(conn, addr, clients):

    conn.send(b"Welcome to this chatroom!")

    while True:
            try:
                message = conn.recv(1024)
                if message:
                    print(message.decode())
                    message_to_send = "<" + clients[conn] + "> " + message.decode()
                    broadcast(message_to_send, conn, clients)
                else:
                    remove(conn, clients)

            except Exception as e:
                print(e)
                continue


def broadcast(message, connection, clients):
    # смотрим есть ли юзер в актив юзерах и отправляем всем кроме него самого
    for client in clients.keys():
        if client != connection:
            try:
                client.sendall(message.encode())
            except:
                remove(connection, clients)

# если юзер вышел удаляем из активных и пишем всем о выходе
def remove(connection, clients):
    if connection in clients:
        left_user = clients[connection]
        del clients[connection]
        user_left(left_user, clients)


def user_joined(connection, clients):
     if connection in clients:
        join_user = clients[connection]
        join_message = f"{join_user} has joined".encode()
        for client in clients.keys():
            if client != connection:
                client.sendall(join_message)


def user_left(user, clients):
    left_message = f"{user} has disconnected".encode()
    for client in clients.keys():
        client.sendall(left_message)


if __name__ == "__main__":
    main()