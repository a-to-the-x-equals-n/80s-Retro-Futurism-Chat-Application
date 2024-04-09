import curses
from curses import textpad
from curses.textpad import rectangle
import util
import time
import threading


username = "Logan"

def chat(stdscr):
    curses.curs_set(0)  # Show the cursor
    stdscr.clear()  # Clear the screen

    # Initialize color pair
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Define color pair 1 with red foreground and black background
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    
    # height = 30
    # width = 120
    
    # Get the size of the screen
    # 30     120
    MAX_X, MAX_Y = stdscr.getmaxyx()
    max_x = MAX_X - 2 # 28
    max_y = MAX_Y - 2 # 118

    # Calculate the height of the top and bottom windows
    chat_max_height = max_x-9  # 23

    rectangle(stdscr, 2, 2, max_x-6, max_y)
    rectangle(stdscr, max_x - 4, 2, max_x, max_y)
    stdscr.refresh()

    # nlines: The number of lines (rows) in the window. This is the height of the window.
    # ncols: The number of columns in the window. This is the width of the window.
    # begin_y: The y-coordinate (row number) of the upper-left corner
    # begin_x: The x-coordinate (column number) of the upper-left corner

    # Create windows for the top and bottom halves
    chat_window = curses.newwin(max_x-9, max_y-4, 3, 4)
    text_entry_window = curses.newwin(3, max_y-4, max_x-3, 3)
    chat_window.scrollok(True)  # Enable scrolling for the top window

    # List to store messages
    messages = []

    # Lock for synchronizing access to the messages list and the screen
    lock = threading.Lock()

    # Define the enter key
    enter_key = ord('\n')

    # Function to accept user input and append it to messages
    def enter_message(x):
        if x == enter_key:
            return 7  # ASCII code for bell, used to terminate textbox.edit()
        else:
            return x


    # Function to display messages in the top window
    @util.threaded
    def display_messages():
        while True:
            with lock:
                chat_window.erase()
                # Use the second color pair for the messages text
                chat_window.attron(curses.color_pair(2))
                # Calculate the index of the first message to display based on the window height
                first_line_index = max(len(messages) - (chat_max_height - 1), 0)
                # Display messages starting from the first_line_index
                for i, msg in enumerate(messages[first_line_index:]):
                    # Make sure not to try writing beyond the drawable area of the window
                    if i < chat_max_height - 1:
                        chat_window.addstr(i, 0, msg)
                chat_window.attroff(curses.color_pair(2))  # Turn off the color attribute
                chat_window.refresh()
            time.sleep(0.1)

    # Create a textbox for input
    textbox = textpad.Textbox(text_entry_window, insert_mode=True)

    # Start the message display thread
    display_messages()

    while True:

        # Clear bottom window and get user input
        text_entry_window.erase()
        text_entry_window.refresh()
        textbox.stripspaces = True
        
        message = textbox.edit(enter_message).strip()
        message = f'[{username}]:~$ {message}'
        
        if message:
            with lock:
                messages.append(message)
                if len(messages) > chat_max_height - 1:
                    # Remove the first item in the list to maintain the display area
                    del messages[0]

            # Manually clear the text box after sending message
            text_entry_window.erase()
            text_entry_window.refresh()

            # Update the display immediately after adding a message
            with lock:
                chat_window.erase()
                chat_window.attron(curses.color_pair(2))
                for i, msg in enumerate(messages[-(chat_max_height - 1):]):
                    chat_window.addstr(i+1, 0, msg)
                chat_window.refresh()
                chat_window.attroff(curses.color_pair(2))  # Turn off the color attribute

curses.wrapper(chat)