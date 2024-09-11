import socket
import time
import cv2
import struct
import pickle

camera = cv2 . VideoCapture (0)

server_socket = socket . socket ( socket . AF_INET , socket . SOCK_STREAM )
server_socket . bind (( '<server ␣ip␣ address >', 5020) )
server_socket . listen (1)
print ('Waiting for connection ... ')

while True :
    client_socket , addr = server_socket . accept ()
    print ( f'Connected ␣to␣{ addr }')

    try :
        while True :
            ret , frame = camera . read ()
            if not ret :
                break

            data = pickle . dumps ( frame )
            message_size = struct . pack ("Q", len ( data ) )
            client_socket . sendall ( message_size + data )
            time . sleep (0.1)

    except ( ConnectionResetError , BrokenPipeError ) :
        print ( f'Connection ␣ with ␣{ addr }␣is␣ terminated .')

    finally :
        client_socket . close ()

    server_socket . close ()
    camera . release ()