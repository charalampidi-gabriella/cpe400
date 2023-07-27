import socket
import tkinter as tk
import authentication
import os

# Socket setup
host = '127.0.0.1'
port = 59000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Authentication
alias = authentication.authenticate()
if alias is None:
    print("User disconnected.")
    os._exit(0)  # terminate

client.send(alias.encode('utf-8'))


