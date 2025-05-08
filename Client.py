import socket
import threading

HOST = "10.120.151.136" # Ip addres of the server (my laptop)
PORT = 12345


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))


#username input

username = input("Enter your username: ")
client.send(username.encode('utf-8'))

#function to receive messages from the server
def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg)
        except:
            print("An error occurred!")
            client.close()
            break

#function to send messages to the server
def send():
    while True:
        try:
            msg = input()
            client.send(msg.encode('utf-8'))
        except:
            print("An error occurred!")
            client.close()
            break

#start the threads for receiving and sending messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()