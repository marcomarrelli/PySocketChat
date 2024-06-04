#!/usr/bin/env python3

import socket
import threading
import logging

from config import Settings

class Server:
    connections: list[socket.socket] = [] # Clients' Socket List.
    serverSocket: socket.socket = None # Server's Socket.

    def __init__(self) -> None:
        '''
            Initializes the Server.
        '''
                
        try:
            logging.basicConfig(level=logging.NOTSET, format='[SERVER - %(levelname)s] %(message)s') # Initialize Logging.

            # Create the Server's Socket and bind it to an address and a port.
            # Then give a maximum of simultaneous connections.
            Server.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Server.serverSocket.bind((Settings.SERVER_ADDRESS, Settings.SERVER_PORT))
            Server.serverSocket.listen(Settings.MAX_NUMBER_OF_CLIENTS)

            logging.info('Server started!')

            # Accepting Clients infinite loop.
            while True:
                serverConnection, address = Server.serverSocket.accept()
                Server.connections.append((serverConnection, address))
                threading.Thread(target=Server.manageClient, args=[serverConnection, address]).start()
        except RuntimeError as e:
            logging.error(f'Error occurred when creating user thread: {e}.')
        except Exception as e:
            logging.error(f'Error occurred when creating socket: {e}.')
        finally:
            # If there are users connected, remove them.
            if Server.connections:
                for conn, addr in Server.connections:
                    Server.removeClient(conn, addr)


    @staticmethod
    def manageClient(connection: socket.socket, address: str) -> None:
        '''
            Send and receive messages from all the users.
        '''
        
        # Clients messages handling infinite loop.
        while True:
            try:
                receivedMessage = connection.recv(Settings.BUFFER_SIZE)
                if receivedMessage:
                    sendingMessage = f'[{address[0]}:{address[1]}] {receivedMessage.decode(Settings.MESSAGE_ENCODING)}'
                    logging.info(sendingMessage)
                    Server.broadcast(sendingMessage, connection)
                else:
                    Server.removeClient(connection, address)
                    break
            except Exception as e:
                logging.error(f'Error occured while handling client {address} connection: {e}.')
                Server.removeClient(connection, address)
                break


    @staticmethod
    def broadcast(message: str, connection: socket.socket) -> None:
        '''
            Send message to all clients.
        '''
        
        # Send a broadcast message, cycling through all clients.
        for clientConnection, _ in Server.connections:
            try:
                clientConnection.send(message.encode(Settings.MESSAGE_ENCODING))
            except Exception as e:
                logging.error(f'Error occured while broadcasting message to client {_}: {e}.')
                Server.removeClient(clientConnection, _)


    @staticmethod
    def removeClient(connection: socket.socket, address: str) -> None:
        '''
            Remove client from the connection list.
        '''
        
        # Removes the selected client from the connections list,
        # then send a broadcast message with that information.
        if connection in [c for c, _ in Server.connections]:
            connection.close()
            Server.connections = [(c, addr) for c, addr in Server.connections if c != connection]
            leavingMessage: str = f'[{address[0]}:{address[1]}] has left the server.'
            Server.broadcast(leavingMessage, connection)
            logging.info(leavingMessage)
        
        # If all users are gone, then close the server.
        if Server.serverSocket and not Server.connections:
            Server.serverSocket.close()
            logging.info('Server closed!')
