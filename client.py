#!/usr/bin/env python3

import socket
import threading
import logging

from tkinter import *
from tkinter import ttk, scrolledtext

from config import Settings

'''
    Main process that start client connection to the server 
    and handle it's input messages
'''
class Client:
    clientSocket: socket.socket = None # Client's Socket.

    def __init__(self, root: Tk) -> None:
        '''
            Initializes the Client and creates its GUI.
        '''

        try:
            logging.basicConfig(level=logging.NOTSET, format='[CLIENT - %(levelname)s] %(message)s') # Initialize Logging.

            # Connects the Client to the Server.
            self.clientSocket = socket.socket()
            self.clientSocket.connect((Settings.SERVER_ADDRESS, Settings.SERVER_PORT))

            # Create the GUI Window.
            # Set it not resizable and the action on close button pressed.
            self.root = root
            self.root.title(Settings.SERVER_NAME)

            # Create the Message Box.
            self.mainWindow = ttk.Frame(self.root, padding=10)
            self.mainWindow.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W))

            # Create the Users Message Area.
            self.messageArea = scrolledtext.ScrolledText(self.mainWindow, wrap='word', state='disabled')
            self.messageArea.grid(row=0, column=0, columnspan=2, sticky=(N, S, E, W))

            # Create the Message Entry.
            self.inputArea = ttk.Entry(self.mainWindow, width=50)
            self.inputArea.grid(row=1, column=0, sticky=(E, W))
            self.inputArea.bind('<Return>', self.sendMessage)

            # Create the Send Message.
            self.sendButton = ttk.Button(self.mainWindow, text="Send", command=self.sendMessage)
            self.sendButton.grid(row=1, column=1, sticky=(E, W))

            self.root.resizable(False, False)
            self.root.protocol("WM_DELETE_WINDOW", self.closeConnection)

            # Starts the manageMessage thread.
            threading.Thread(target=self.manageMessage, args=[self.clientSocket], daemon=True).start()

            logging.info('Connected to chat')

        except Exception as e:
            logging.error(f'Error connecting to server socket: {e}', exc_info=True)
            self.clientSocket.close()
            root.destroy()


    def manageMessage(self, connection: socket.socket):
        '''
            Retrieve messages from the server.
        '''
        
        # Message Management infinite loop.
        while True:
            try:
                msg = connection.recv(Settings.BUFFER_SIZE)
                if msg:
                    self.displayMessage(msg.decode(Settings.MESSAGE_ENCODING))
                else:
                    connection.close()
                    break
            except Exception as e:
                logging.error(f'Error handling message from server: {e}', exc_info=True)
                connection.close()
                break


    def displayMessage(self, msg: str):
        '''
            Display received messages to the client's GUI.
        '''
        
        # Add the message to the text area.
        self.messageArea.configure(state='normal')
        self.messageArea.insert(END, msg + '\n')
        self.messageArea.configure(state='disabled')
        self.messageArea.yview(END)


    def sendMessage(self, event: None = None):
        '''
            Send message to the server.
        '''
        
        # Get the message entry and send it as an encoded message.
        msg = self.inputArea.get()
        if not msg:
            return
        try:
            self.clientSocket.send(msg.encode(Settings.MESSAGE_ENCODING))
            self.inputArea.delete(0, END)
        except Exception as e:
            logging.error(f'Error occured when sending message: {e}.', exc_info=True)


    def closeConnection(self, event: None = None):
        '''
            Close client's connection to the server.
        '''
        
        try:
            self.clientSocket.close()
        except Exception as e:
            logging.error(f'Error occured while closing socket: {e}.', exc_info=True)

        self.root.quit()


    @staticmethod
    def startClientGUI():
        '''
            Starts the client's GUI.
        '''
            
        root = Tk()
        Client(root)
        root.mainloop()


if __name__ == "__main__":
    Client.startClientGUI()