import socket
import datetime
import random
from protocol import *  # Import protocol functions for handling message format

# Set up the server socket
server_socket = socket.socket()  # Create a socket object
server_socket.bind(('0.0.0.0', 1234))  # Bind to all interfaces on port 1234
server_socket.listen(1)  # Set the socket to listen for incoming connections
print(f"server is up at {server_socket.getsockname()}")
while True:
    try:
        # Accept an incoming client connection
        client_socket, client_address = server_socket.accept()  # Accept a client connection
        print(f"client connected at {client_address}")

        # Receive the initial command from the client
        data = client_socket.recv(3).decode()  # Receive up to 3 bytes (command message)
        print(f"request from client: {data}")
        length, msg = read_protocol_message(data)  # Decode the protocol message

        # Process client commands until 'E' (Exit) is received
        while msg != 'E':
            ans = ''  # Variable to store the server's response

            # Check client command and respond accordingly
            if msg == 'T':  # 'T' command for time
                ans = str(datetime.datetime.now())  # Respond with current date and time
            if msg == 'N':  # 'N' command for server name
                ans = 'ORWIES7'  # Respond with the server name
            if msg == 'R':  # 'R' command for random number
                ans = str(random.randint(1, 10))  # Respond with a random integer between 1 and 10
            if msg == '':  # Empty message indicates connection loss
                print('lost connection with client')
                break

            # Prepare and send the response message
            length_text = build_message_len_text(ans)  # Build a 2-digit message length prefix
            client_socket.send(length_text.encode('utf-8'))  # Send the message length to the client
            client_socket.send(ans.encode('utf-8'))  # Send the actual message content

            # Receive the next command from the client
            data = client_socket.recv(3).decode()  # Receive up to 1024 bytes from the client
            print(f"request from client: {data}")
            length, msg = read_protocol_message(data)  # Decode the next protocol message

        # Close the client and server sockets
        print(f"client at {client_address} disconnected")
        client_socket.close()  # Close the connection with the client
    except:
        pass
server_socket.close()  # Close the server socket
