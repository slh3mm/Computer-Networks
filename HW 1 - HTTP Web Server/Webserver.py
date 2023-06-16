#import socket module
from socket import *
import socket
import sys # In order to terminate the program
import os

# def send_file(connection, data):
#     for i in range(0, len(data)):
#         connection.send(data[i].encode())
#     #connection.send("\r\n".encode())
    
serverSocket = socket.socket(AF_INET, SOCK_STREAM) #Prepare a sever socket
port = 6789
host = socket.gethostname()
ip_addr = gethostbyname(host)
serverSocket.bind(('', port))
serverSocket.listen(1)

while True:
    #Establish the connection 
    print('Ready to serve...') 
    connectionSocket, address = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket 
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        #Send lines.
        connectionSocket.send(outputdata.encode()) 

        #Close client socket
        connectionSocket.close()

    #Send response message for file not found
    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>".encode())

        #Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data