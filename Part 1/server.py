#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 01:50:07 2020

@author: sahilsodhi
"""

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def RepresentsInt(s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    
    def send(self, text):
        self.request.sendall(bytes(text + "\n", "utf-8"))
    
    d = {}
    with open("data.txt") as f:
        for line in f:
            (name, age, address, phone) = line.split('|')
            if(name.strip() != ''):
                d[name.strip()] = [age.strip(), address.strip(), phone.strip()]

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip() 
        choice = self.data.decode("utf-8")
        
        if choice == '1':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            resp = ''
            if userName in MyTCPHandler.d:
                resp += '[OK 200]Customer name: ' + userName +"\n"
                [age, address, phone] = MyTCPHandler.d[userName]
                resp += 'Customer Age: ' + age +"\n"
                resp += 'Customer Address: ' + address +"\n"
                resp += 'Customer Phone Number: ' + phone
            else:
                resp += '[OK 200]customer not found'
            MyTCPHandler.send(self, resp)
        
        if choice == '2':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            if(userName == ''):
                MyTCPHandler.send(self, '[OK 200]username cannot be empty')
            elif(userName in MyTCPHandler.d):
                MyTCPHandler.send(self, '[OK 200]Customer already exists')
            else:
                MyTCPHandler.send(self, 'Enter age of the customer')
                age = self.request.recv(1024).strip().decode("utf-8")
                if not MyTCPHandler.RepresentsInt(age):
                    MyTCPHandler.send(self, '[OK 200]Age should be a number.')
                else:
                    MyTCPHandler.send(self, 'Enter address of the customer')
                    address = self.request.recv(1024).strip().decode("utf-8")
                    MyTCPHandler.send(self, 'Enter phone number of the customer')
                    phone = self.request.recv(1024).strip().decode("utf-8")
                    MyTCPHandler.d[userName.strip()] = [age.strip(), address.strip(), phone.strip()]
                    MyTCPHandler.send(self, '[OK 200]Customer record added successfully')
                
        if choice == '3':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            if userName in MyTCPHandler.d:
                MyTCPHandler.d.pop(userName.strip(), None)
                MyTCPHandler.send(self, '[OK 200]Customer record deleted')
            else:
                MyTCPHandler.send(self, '[OK 200]Customer does not exist')
        
        if choice == '4':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            if userName in MyTCPHandler.d:
                MyTCPHandler.send(self, 'Enter new age of the customer: ')
                newAge = self.request.recv(1024).strip().decode("utf-8")
                if not MyTCPHandler.RepresentsInt(newAge):
                    MyTCPHandler.send(self, '[OK 200]Age should be a number.')
                else:
                    MyTCPHandler.d[userName.strip()][0] = newAge
                    MyTCPHandler.send(self, '[OK 200]Customer age updated successfully')
            else:
                MyTCPHandler.send(self, '[OK 200]Customer does not exist')
        
        if choice == '5':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            if userName in MyTCPHandler.d:
                MyTCPHandler.send(self, 'Enter new address of the customer: ')
                newAddress = self.request.recv(1024).strip().decode("utf-8")
                MyTCPHandler.d[userName.strip()][1] = newAddress
                MyTCPHandler.send(self, '[OK 200]Customer address updated successfully')
            else:
                MyTCPHandler.send(self, '[OK 200]Customer does not exist')
        
        if choice == '6':
            MyTCPHandler.send(self, 'Enter name of the customer: ')
            self.data = self.request.recv(1024).strip()
            userName = self.data.decode("utf-8")
            userName = userName.strip()
            if userName in MyTCPHandler.d:
                MyTCPHandler.send(self, 'Enter new phone number of the customer: ')
                newPhone = self.request.recv(1024).strip().decode("utf-8")
                MyTCPHandler.d[userName.strip()][2] = newPhone
                MyTCPHandler.send(self, '[OK 200]Customer phone number updated successfully')
            else:
                MyTCPHandler.send(self, '[OK 200]Customer does not exist')
        
        if choice == '7':
            res = '[OK 200]'
            for i in sorted(MyTCPHandler.d):
                res += 'Customer name: ' + i + '\n'
                [age, address, phone] = MyTCPHandler.d[i]
                res += 'Age: ' + age + '\n'
                res += 'Address: ' + address + '\n'
                res += 'Phone Number: ' + phone + '\n\n'
            MyTCPHandler.send(self, res)
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
        