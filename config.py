#!/usr/bin/env python3

class Settings:
    '''
        Configuration Class.
        Be Careful modifying those values.
    '''
    
    SERVER_NAME: str = 'Unibo Project Server'
    SERVER_ADDRESS: str = '127.0.0.1'
    SERVER_PORT: int = 12500

    NUMBER_OF_CLIENTS: int = 3
    MAX_NUMBER_OF_CLIENTS: int = 10

    BUFFER_SIZE: int = 1024

    MESSAGE_ENCODING: str = "utf8"

    EXCEPTIONS_INFO: bool = False
