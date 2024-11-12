import socket
import threading
import rsa

choice = input("Do you want to host (1) or to connect (2) :")
if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.43.87", 9999))
    server.listen()

    client, _ = server.accept()

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.43.28", 9999))
else:
    exit()


def sending_massages(c):
    while True:
        massage = input("")
        c.send(massage.encode())
        print("You: " + massage)


def receiving_massages(c):
    while True:
        print("partner: " + c.recv(1024).decode())


threading.Thread(target=sending_massages, args=(client,))
threading.Thread(target=receiving_massages, args=(client,))





