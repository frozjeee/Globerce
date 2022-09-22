import msvcrt
import socket

def main():
    HOST = "localhost"
    PORT = 5678
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    print("Type in your nickname:")
    nickname = input()

    sock.connect((HOST, PORT))
    sock.sendall(nickname.encode())

    while True:
        try:
            message = (sock.recv(1024)).decode()
            print(message)
        # на каждый таумаут чекаем если юзер нажал на клаву и он начинает писать. В остальное время не блокаем клавой и ждем сообщения или выход/вход из чата
        except socket.error:
            if msvcrt.kbhit():    
                message = input("<Me> ")
                sock.sendall(message.encode()) 
            else:
                continue


if __name__ == "__main__":
    main()