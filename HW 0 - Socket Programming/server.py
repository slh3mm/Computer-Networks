import socket
import re

#Create a name & choose a number
server_name = "Ewing G. Simpson"
server_num = 12

#Begin accepting connections from clients
host = socket.gethostname()
port = 5001

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(2)
connection, address = server_socket.accept()

while True:
    data = connection.recv(1024).decode()
    if not data: break
    #Print client name
    client_name = ''.join(i for i in data if not i.isdigit())
    print("The server of " + server_name + " is communicating with the client of " + client_name)
    
    #Display client number, server number, and sum
    client_num = int(''.join([i for i in data if i.isdigit()]))
    if client_num <= 1 or client_num >= 100:
        break
    sum = client_num + server_num
    print(str(client_num) + " " + str(server_num) + " " + str(sum))

    #Send name string and server number
    string = server_name + " " + str(server_num)
    connection.send(string.encode())

connection.close()