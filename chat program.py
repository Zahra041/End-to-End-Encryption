import socket
import threading
import rsa
import tkinter as tk

public_key,private_key = rsa.newkeys(1024)
public_partner =None

choice = input("Do you want to host (1) or to connect (2) :")
if choice == "1":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("192.168.43.87",9999))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("192.168.43.28",9999))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1(""))

else:
    exit()

def send_message():
    message = entry.get() # get the message from the entry widget
    client.send(rsa.encrypt(message.encode(),public_partner)) # encrypt and send the message
    text.insert(tk.END, "\nYou: " + message) # insert the message in the text widget
    entry.delete(0, tk.END) # clear the entry widget

def receive_message():
    while True:
        message = rsa.decrypt(client.recv(1024), private_key).decode() # decrypt and decode the message
        text.insert(tk.END, "\nPartner: " + message) # insert the message in the text widget

root = tk.Tk() # create the root window
root.title("Chat Application") # set the title of the window

text = tk.Text(root) # create the text widget
text.grid(row=0, column=0, columnspan=2) # place the text widget in the grid

entry = tk.Entry(root) # create the entry widget
entry.grid(row=1, column=0) # place the entry widget in the grid

button = tk.Button(root, text="Send", command=send_message) # create the button widget
button.grid(row=1, column=1) # place the button widget in the grid

threading.Thread(target=receive_message) # start the thread for receiving messages

root.mainloop() # start the main loop of the window
