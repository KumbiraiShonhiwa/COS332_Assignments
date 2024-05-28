import hashlib
import os
import socket
import re
import time


def calculate_hash(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def send_command(s, command):
    s.sendall((command + '\r\n').encode())
    response = s.recv(1024).decode()
    print('Received:', response)
    return response


def download_file(s, data_socket, filename,data):
    send_command(s, 'RETR ' + '/protected/file.txt')
    with open(filename, 'w') as f:
        f.write(data)


server = "127.0.0.1"
username = "Kumbirai"
password = "ArisNeiman123#"
filename = "file.txt"

    
original_hash = calculate_hash(filename)
original_hash = 1

while True:
    current_hash = calculate_hash(filename)
    with open(filename, 'w') as f:  
        f.write('Hello, World!')
    if current_hash != original_hash:
        print('File has been modified, downloading original file...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, 37992))
            send_command(s, 'USER ' + username)
            send_command(s, 'PASS ' + password)
            send_command(s, 'TYPE I')
            response = send_command(s, 'PASV')
            try:
                download_file(s, 21, filename,'hello world')
                original_hash = calculate_hash(filename)
                print('File has been restored.')
            except PermissionError:
                print('File is currently being edited, will try again later.')

            send_command(s, 'QUIT')

    time.sleep(6)  # check every minute
