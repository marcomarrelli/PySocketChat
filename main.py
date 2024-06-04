#!/usr/bin/env python3

"""
    Traccia 1: Sistema di Chat Client-Server.
    
    Implementare un sistema di chat client-server in Python
    utilizzando socket programming.
    Il server deve essere in grado di gestire più client contemporaneamente
    e deve consentire agli utenti di inviare
    e ricevere messaggi in una chatroom condivisa.
    Il client deve consentire agli utenti di connettersi al server,
    inviare messaggi alla chatroom
    e ricevere messaggi dagli altri utenti.
"""

import threading

from client import Client
from server import Server
from config import Settings

if __name__ == "__main__":    
    # Checks if some settings values are wrong and corrects them.
    if Settings.NUMBER_OF_CLIENTS < 2:
        Settings.NUMBER_OF_CLIENTS = 2
    elif Settings.NUMBER_OF_CLIENTS > Settings.MAX_NUMBER_OF_CLIENTS:
        Settings.NUMBER_OF_CLIENTS = Settings.MAX_NUMBER_OF_CLIENTS
    if Settings.BUFFER_SIZE < 0:
        Settings.BUFFER_SIZE = 1024

    # Start the Server Thread.
    threading.Thread(target=Server).start()
    
    # Start the Client Threads.
    for _ in range(Settings.NUMBER_OF_CLIENTS):
        threading.Thread(target=Client.startClientGUI).start()
