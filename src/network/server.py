import socket

HOST = "192.168.15.62"
PORT = 9999


def server(me):
    svr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svr.bind((HOST, PORT))
    svr.listen()
    while True:
        communication_socket, address = server.accept()
        print(f"Connected to {address}")
        message = communication_socket.recv(1024).decode("utf-8")
        print(f"Message:   {message}")
        communication_socket.send(
            f"{me}:: Received your message! Thank you".encode("utf-8")
        )
        communication_socket.close()
        print(f"Communication with {address} ended")
