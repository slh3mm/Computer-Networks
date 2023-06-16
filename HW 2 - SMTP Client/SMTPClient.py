
#!/usr/bin/env python3

# Include needed libraries. Do _not_ include any libraries not included with
# Python3 (i.e. do not use `pip` use 'pip3' instead of installs).
import socket

# Establish a TCP connection with the mail server.
s = socket.socket()
local = '10.0.0.94'
loopback = '127.0.0.1'
s.connect((loopback, 25))
Buffer = 4096

# Read greeting from the server
response = s.recv(Buffer).decode('utf-8')

# if not response.startswith('220'):
# 	raise Exception('220 reply not received from server.')

# Send HELO command and get server response.
cmd_HELO = 'HELO alice\r\n'
print(cmd_HELO)
s.send(cmd_HELO.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# if not response.startswith('250'):
#     raise Exception('250 reply not received from server.')


# Send MAIL FROM command.
cmd_MAILFROM = 'MAIL FROM: <slh3mm@virginia.edu>\r\n'
print(cmd_MAILFROM)
s.send(cmd_MAILFROM.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# Send RCPT TO command. You will send to <sys> which account on the VM.
cmd_RCPT = 'RCPT TO: <sys>\r\n'
print(cmd_RCPT)
s.send(cmd_RCPT.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# Send DATA command.
cmd_DATA = 'DATA\r\n'
print(cmd_DATA)
s.send(cmd_DATA.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# Send message data.
cmd_MSG = 'Hello, World!\r\n'
print(cmd_MSG)
s.send(cmd_MSG.encode())

# response = s.recv(Buffer).decode('utf-8')
# print(response)

# End with line with a single period.
cmd_PD = '.\r\n'
print(cmd_PD)
s.send(cmd_PD.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# Send QUIT command.
cmd_QUIT = 'QUIT\r\n'
print(cmd_QUIT)
s.send(cmd_QUIT.encode())

response = s.recv(Buffer).decode('utf-8')
print(response)

# Close the socket when finished.
s.close()
