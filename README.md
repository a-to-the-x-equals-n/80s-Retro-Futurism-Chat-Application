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

### System Requirements
```bash
Python 3.x
curses
```

- The program uses ANSI escape codes and the `curses` library to manipulate cursor positioning and text animations.
- It requires a terminal that supports ANSI escape codes for full functionality.
- For best results, execute the program in a linux based terminal, such as `Ubuntu`.  The program was written and testing in a WSL `Ubuntu` terminal.
- It's recommended to leave the terminal window at it's default size.

### Quick Start Guide

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
## `main.py`
### Logging
- The application now logs all significant events and errors to `app.log`, aiding in debugging and operational monitoring. Use `tail -f app.log` to view log output in real time.

### Dynamic GUI and Threading
- Utilizes the `GUI` class as a context manager to ensure clean setup and teardown.  
    (*The* `curse` *library desyncs the terminal window quite frequenty, so encapsulating and isolating all* `curse` *implementations became necessary to maintain successful operations.*)
- Implements threading to concurrently execute user interfaces and backend tasks, improving the overall program responsiveness and user experience.

### Network Operations
- Depending on user selection, acts as either a HOST or a CLIENT, managing connections accordingly.
- Custom error handling techniques are in place to handle any network-related exceptions, ensuring the application remains stable and responsive.

### Terminal Compatibility
- Adjusts to terminal dimensions at startup, ensuring optimal display and functionality.

### Functions

- `main()`: The main function to initialize the program.
- `welcome_screen(x,y)`: Animates the 'Dark Tunnel' ASCII art.
- `morph`: Animates Morpheus in ASCII art -- a fun litte way to pay homage to the OG inspirators.
- The main function also handles the type of user and passes those values along to the chat functionality.

## `user.py`

### Initialization
- The `User` class now supports default and customizable settings for IP address, port number, and username. Each user object is initialized with a socket ready for network communications.

### Socket Handling
- Each user manages a dedicated socket for sending and receiving data over the network. This encapsulation enhances the modularity and reusability of the network code.

### Server and Client Modes
- **Listening Mode**: Users can act as servers, listening for incoming connections using the `listening` method, which binds the socket to the designated IP and port.
- **Searching Mode**: In client mode, the `searching` method prepares the user to connect by retrieving the server address, facilitating easy connection setup.

### Utilities
- The class includes utility methods like `__str__` and `__len__` for convenient representation and length checking of the user's username, primarily used for logging and user interface display.

### Creating a User
```python
# Create a user with default settings
default_user = User()

# Create a user with custom settings
custom_user = User(ip='192.168.1.1', port=12345, username='john_doe')

# Setup a user to act as a server
server_user = User()
server_user.listening()

# Setup a user to act as a client
client_user = User(ip='192.168.1.1', port=12345)
server_address = client_user.searching()
```
## `util.py`

### Thread Management
- The `@threaded` decorator allows functions to be executed in separate threads, improving the application's responsiveness and performance.

### Terminal Compatibility and Utilities
- **Terminal Size**: Employs `Shutil` to gather the terminal size -- instead of `curses`, ensuring optimal layout and display.
- **Clear Terminal**: Provides a method to clear the terminal screen, supporting both Windows and POSIX systems.

### Visual Effects
- **Text Fading**: Implements fading effects for text display, which include:
  - `fade_out`: Fades text out by decreasing its color intensity.
  - `fade_in`: Fades text in by increasing its color intensity.
  - `fade_text`: Applies a fade effect to text using specified RGB color values.

### ASCII Art
- Features several ASCII art designs (`morpheus`, `dark`, `tunnel`) to enhance the aesthetic appeal of the application's interfaces.

## `gui.py`

### Overview

- **Curses GUI Handling**: Implements a comprehensive GUI system using curses, which handles terminal window drawing, user input, and more.
- **Multithreading for Animation and Input Handling**: Utilizes threading to manage animations and asynchronous input processing simultaneously.
- **Animated Text Effects and Welcome Screen**: Features animated text displays for both welcoming users and during operations like connection and message handling.
- **User Interaction Through GUI**: Allows users to join sessions, host sessions, and handle errors within the GUI.
- **Chat Functionality**: Manages a chat interface where messages are sent and received, including display handling for incoming and outgoing messages.

### Curses Interface
- The application uses the `curses` library extensively to create a responsive, text-based user interface that supports multiple windows and real-time updates.

### Welcome Screen and Text Animations
- Implements dynamic welcome screens with animated text effects using the ASCII art and fading functionalities from the `util` module.

### Interactive Session Handling
- Users can choose to join an existing session, host a new session, or exit directly from the initial screen. These actions are handled interactively using `curses` buttons and inputs.

### Chat Interface
- Features a dedicated chat window where messages are continuously received and displayed. The chat system also supports real-time message sending with a responsive text input area.

### Error Handling
- Integrated error display mechanism that provides feedback directly within the GUI for issues like invalid input or connection problems.

### Navigation
- Use arrow keys for navigation between the session join, host, and exit options on the initial screen.
- Press `Enter` to select an option

### Exiting
- To exit the chat or the application, follow the on-screen instructions which may include typing special commands or using interface buttons.