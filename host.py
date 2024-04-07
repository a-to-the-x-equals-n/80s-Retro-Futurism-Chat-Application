import os
from pathlib import Path
import socket as s
import time


def handle_request(client_socket):

    # Receive the HTTP request from the client
    request = client_socket.recv(1024).decode()
    

    # Extract the path of the requested file from the HTTP request
    try:

        filename = request.split()[1].strip("/")
        

    except IndexError:

        # Bad Request
        client_socket.sendall("HTTP/1.1 400 Bad Request\r\n\r\n".encode())

        client_socket.close()


    
    # Construct the full path of the requested file
    filepath = ABSOLUTE_PATH / filename
    
    # Check if the file exists
    if filepath.exists():

        # If the file exists, read its contents
        with open(filepath, "rb") as file:

            file_content = file.read()


        # Send the HTTP response with status code 200 (OK) and the file content
        response = "HTTP/1.1 200 OK\r\n\r\n".encode() + file_content

        client_socket.sendall(response)


    else:

        # If the file does not exist, send an HTTP response with status code 404 (Not Found)
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found.".encode()

        client_socket.sendall(response)


    # Close the client socket
    client_socket.close()



def main():


    # Create socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)


    # Binds 'server_socket' to the host IP and port number
    server_socket.bind((HOST, PORT))


    # Listening socket
    server_socket.listen(1)

    # Timeout set to 30 seconds
    server_socket.settimeout(30)  


    try:

        while listening:

            # Accept incoming connection
            client_socket, client_addr = server_socket.accept()

            print(f"Connection from {client_addr}")

            # Handle the incoming request
            handle_request(client_socket)

            listening = False

    # Handles when HAL goes back to sleep
    except s.timeout:

        print("TIMEOUT: HAL 9000 went back to sleep...")

    finally:

        # Close the server socket
        server_socket.close()


if __name__ == "__main__":

    HOST = 'localhost'
    PORT = 8080
    ABSOLUTE_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
    

    main()
