import socket
import sys
import re

#Accept command line argument
client_num = int(sys.argv[1])

#Open a TCP Socket to the server
host = socket.gethostname()
port = 5001

client_socket = socket.socket()
client_socket.connect((host, port))

#Send a message of the client name
client_name = "Thomas M. Taylor"
message = client_name + " " + str(client_num)
client_socket.send(message.encode())

data = client_socket.recv(1024).decode()
server_num = int(''.join([i for i in data if i.isdigit()]))
sum = client_num + server_num
print("Sum of values: " + str(sum))

client_socket.close()