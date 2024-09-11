import socket
import cv2
import struct
import pickle

 
client_socket = socket . socket ( socket . AF_INET , socket . SOCK_STREAM )
server_address = ('192.168.11.46', 5020)
client_socket . connect ( server_address )
print ( f'Connected ␣to␣ server ␣at␣{ server_address }')

data = b""
info_size = struct.calcsize("Q")
try:
    while True:
        while len(data) < info_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        info = data[:info_size]
        data = data[info_size:]
        data_size = struct.unpack("Q", info)[0]

        while len(data) < data_size:
            data += client_socket.recv(4096)
        frame_data = data[:data_size]
        data = data[data_size:]

        frame = pickle.loads(frame_data)

        cv2.imshow('Received Image', frame)

except ( ConnectionRefusedError , ConnectionResetError ,BrokenPipeError , TimeoutError ) as e:
    print ( f'Connection error : {e}')

finally:
    client_socket . close ()
    cv2.destroyAllWindows()