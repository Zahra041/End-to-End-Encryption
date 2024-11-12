import socket
import threading
import rsa


public_key,private_key = rsa.newkeys(1024)
public_partner =None

choice = input("Do you want to host (1) or to connect (2) :")
if choice == "1":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("192.168.43.87",9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1(""))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.43.28",9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1(""))

else:
    exit()

def sending_massages(c):
    while True:
        massage = input("")
        c.send(rsa.encrypt(massage.encode(),public_partner))
        print("You: "+massage)

def receiving_massages(c):
    while True:
        print("partner: " + rsa.decrypt(c.recv(1024), private_key).decode())

threading.Thread(target=sending_massages, args=(client,))
threading.Thread(target=receiving_massages, args=(client,))

