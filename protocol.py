# Dictionary that maps command shortcuts to their full names.
commands = {
    'T': 'Time',  # 'T' command for getting the time
    'N': 'Name',  # 'N' command for getting the name
    'R': 'Rand',  # 'R' command for generating a random value
    'E': 'Exit'  # 'E' command for exiting the program
}


def build_message_len_text(message):
    """
    Builds a string representing the length of a message, padded to 2 digits with leading zeros.

    Args:
        message (str): The message whose length will be calculated.

    Returns:
        str: A 2-digit string representing the length of the message, with leading zeros if necessary.
    """
    return f"{len(message):0>2}"


def build_protocol_message(message):
    """
    Builds a protocol message by prepending the message length to the message.

    Args:
        message (str): The message to be formatted.

    Returns:
        str: The formatted protocol message, where the first two characters represent the message length,
             followed by the actual message content.
    """
    return f"{len(message):0>2}{message}"


def read_protocol_message(formatted_msg):
    """
    Reads and parses a protocol message, extracting the length and content.

    Args:
        formatted_msg (str): The protocol-formatted message, where the first two characters represent
                             the length of the message.

    Returns:
        tuple: A tuple (int, str) where the first element is the length of the message, and the second
               element is the message content.
    """
    length = formatted_msg[0:2]  # Extracts the length portion of the message
    msg = formatted_msg[2:]  # Extracts the actual message content
    return int(length), msg


def build_command_text():
    """
    Builds a formatted text displaying command options for user input.

    Returns:
        str: A prompt string showing available command options and their shortcuts, asking the user
             to enter a choice.
    """
    text = "Enter your choice: "
    commands_text = ""
    for key, value in commands.items():
        commands_text += f"{value}({key}) "
    text += commands_text + ": "
    return text