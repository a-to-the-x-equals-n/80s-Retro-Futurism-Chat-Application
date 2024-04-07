# 80s Retro Futurism Chat App
### ( *Currently Under Development* )
This project was inspired by an assignment I had as an undergrad at East Carolina University. I went a bit beyond the scope of the assignment, as I wanted to explore the nostalgic terminal based graphical interfaces, as well as more complex network interactions. A brief summary of the orignal assignment guidelines, are found in the section titled **Original Assignment**.

## Original Assignment

### Instructions
"*In this project, you will develop a Python-based chat application facilitating text messaging between a* `server` *and a* `client`. *Utilize the* `socket` *module for network communication.*"

### Server Specifications
- **Initialization**: Prompt user for an IP address (defaults to localhost) and port number (defaults to predefined port).
- **Username**: Request a username from the user.
- **Conversation Display**: Show both server and client usernames alongside their messages.
- **Operation**: After setup, the server waits for a client's connection. After a connection is established, messages can be shared between server and client.
- **Termination**: The application shuts down if an exit keyword (e.g., "end") is entered by either party.

### Client Specifications
- **Connection**: Connect to the server using the provided IP address and port number.
- **Messaging**: Allow users to send messages between the server and client. All messages are displayed to both endpoints. The communication loop continues until the exit keyword is entered.
- **Error Handling**: Implement error handling for scenarios like invalid IP/port entry, connection issues, or empty message strings. 

## Getting Started

This guide outlines how to set up a Python virtual environment to run this application.  This progam is ideal for Linux environments.

### Requirements
```bash
Python 3.x
curses
python-dotenv
```

### Establish Environment

Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Packages

Install all packages listed in `requirements.txt`.

```bash
pip3 install -r requirements.txt
```

### Run Program

```bash
python3 main.py
```

### Deactivate the Virtual Environment

Once you're done, you can deactivate the virtual environment by running:
```bash
deactivate
```

# Program Outline
## Description

The program displays animated text effects in terminal using ANSI escape codes.  This serves as the welcome screen upon running the application.

The program consists of the following components:

- `main()`: The main function to initialize the program.
- `init_screen(x, y)`: Function to initialize the screen with animated text effects.
- `tunnel(x, y)`: Animates 'tunnel'.
- `dark(x, y)`: Animates 'dark' text.

## Usage Notes

- The program uses ANSI escape codes to manipulate the cursor position and text color.
- It requires a terminal that supports ANSI escape codes for full functionality.