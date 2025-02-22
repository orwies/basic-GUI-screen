import socket
from protocol import *  # Import protocol functions from an external module


def get_data(data=""):
    """
    Returns the provided data. This function currently serves as a placeholder
    and does not perform any additional processing.

    Args:
        data (str): The data to be returned.

    Returns:
        str: The same data that was provided as input.
    """
    return data


def main():
    """
    Main function to run the client-side program.

    - Establishes a socket connection to a server on localhost (IP: 127.0.0.1, Port: 1234).
    - Sends commands to the server based on user input and displays server responses.
    - Uses a simple protocol for message formatting, where the command is sent with
      a prefixed length, and the server response is parsed to retrieve the message length and content.

    Commands:
        - 'T' for Time: Requests the current time from the server.
        - 'N' for Name: Requests the server name.
        - 'R' for Random: Requests a random value from the server.
        - 'E' for Exit: Ends the connection and closes the client.
    """
    client_socket = socket.socket()  # Initialize the client socket
    client_socket.connect(('127.0.0.1', 1234))  # Connect to the server
    # --------------------------------------------------
    command = build_command_text()  # Build command prompt text for user input

    data = input(command)  # Get initial command input from the user
    data = data.upper()  # Convert input to uppercase to ensure case-insensitive commands

    while data != 'E':  # Loop until the user enters the 'Exit' command
        if data == 'T' or data == 'N' or data == 'R':
            # Format the command into a protocol message and send it
            data = build_protocol_message(data)
            print("sending:", data)
            client_socket.send(data.encode('utf-8'))

            # Receive the message length from the server
            response = client_socket.recv(2).decode('utf-8')
            length = int(response)  # Convert length to an integer
            # Receive the actual message based on the specified length
            msg = client_socket.recv(length).decode('utf-8')
            print(f"response: {length} : {msg}")
        elif data != 'E':
            # Inform the user if the input command is invalid
            print("Incorrect input value")

        # Prompt the user for another command
        data = input(command)
        data = data.upper()

    # Handle 'Exit' command to close the connection
    print("sending:", data)
    client_socket.send(data.encode('utf-8'))
    print('Exiting ...')
    client_socket.close()  # Close the client socket


# Run the main function if this file is executed directly
if __name__ == "__main__":
    main()