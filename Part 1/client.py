#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 01:55:59 2020

@author: sahilsodhi
"""

import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

# Create a socket (SOCK_STREAM means a TCP socket)
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        choice = input("""
           1. Find customer\n
           2. Add customer\n
           3. Delete customer\n
           4. Update customer age\n
           5. Update customer address\n
           6. Update customer phone\n 
           7. Print report\n
           8. Exit\n
           Enter your choice: """)
        choice = choice.strip()
        if not RepresentsInt(choice) or int(choice) < 1 or int(choice) > 8:
            print('Please enter a number from 1-8')
            continue
        if choice == '8':
            print('Good Bye')
            break
        sock.sendall(bytes(choice + "\n", "utf-8"))
        # Receive data from the server and shut down
        received = str(sock.recv(4096), "utf-8")
        while True:
            if received.startswith('[OK 200]'):
                break
            else:
                userChoice = input(format(received))
                sock.sendall(bytes(userChoice + "\n", "utf-8"))
                received = str(sock.recv(1024), "utf-8")   
        print(format(received[8:]))
        