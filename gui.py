import curses
import util
import time
from curses import textpad
from curses.textpad import rectangle
import threading
from user import User
import sys


def welcome_screen(x,y):
    """
    Initialize the screen with animated text effects.

    Args:
        x (int): The number of rows in the terminal.
        y (int): The number of columns in the terminal.
    """
    # Start two threads to animate 'tunnel' and 'dark' text concurrently.
    tunnel_thread = tunnel(x//2,y)
    dark_thread = dark(x//2,y)

    # Wait for both animation threads to complete before proceeding.
    tunnel_thread.join()
    dark_thread.join()

    # Combine the 'dark' and 'tunnel' ASCII art for display.
    dark_tunnel_display = []
    dark_tunnel_display.extend(util.dark.split('\n'))
    dark_tunnel_display.extend(util.tunnel.split('\n'))

   # Calculate the starting row for display and initialize the color step.
    start = x//2-6
    step = 0
    while step < 255:
        util.clear() # Clear the terminal for fresh animation frame.
        sys.stdout.flush()  # Flush the buffer to ensure immediate printing

        # Display each line of the combined ASCII art with color fading effect.
        for row, line in enumerate(dark_tunnel_display):
            cursor = f"\033[{start+row};{39}H"
            sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))
        time.sleep(0.2)
        step+=30

        # Prompt the user to press Enter with a fading effect on the text color.
        sys.stdout.write(f"\033[{x//2};{y//2-10}H" + util.fade_text(f"-[PRESS ENTER]-", red = 0, green = step, blue = step//2))

    # Display the final prompt to press Enter with full color.
    sys.stdout.write(f"\033[{x//2};{y//2-10}H" + util.fade_text(f"-[PRESS ENTER]-", red = 0, green = 255, blue = step//2))
    
    # Wait for user to press `Enter`
    input()

@util.threaded
def tunnel(x, y):
    """
    Animate 'tunnel' ASCII art text in a sliding and fading effect. This function runs in a separate thread
    to allow simultaneous execution with other processes.

    Args:
        x (int): The starting row position for the animation.
        y (int): The starting column position for the animation.
    """
    tunnel = util.tunnel.split('\n') # Split the ASCII art into individual lines for processing.
    start = x # Initialize the starting position for the animation.
    step = 0 # Initialize color intensity step.

    # Loop to create a sliding effect from right to left.
    for i in range(0, y//3, 3):
        util.clear() # Clear the terminal before displaying the next frame.

        # Loop through each line of the ASCII art.
        for row, line in enumerate(tunnel):
            cursor = f"\033[{start+row};{y-42-i}H" # Position the cursor for each line.
            sys.stdout.write(cursor + util.fade_text(line, step, 0, step)) # Write the faded text to the terminal.
        
        sys.stdout.flush()  # Ensure that all output is written to the terminal.
        time.sleep(0.3) # Delay to slow down the animation.
        step+=15 # Increase the intensity step for the next frame.

    # Final frame to ensure the text remains visible at the end of the animation.
    for row, line in enumerate(tunnel):
            cursor = f"\033[{start+row};{y-42-i}H"
            sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))

@util.threaded
def dark(x, y):
    """
    Animate 'dark' ASCII art text in a sliding and fading effect. This function runs in a separate thread
    to allow simultaneous execution with other processes.

    Args:
        x (int): The starting row position for the animation.
        y (int): The starting column position for the animation.
    """
    dark = util.dark.split('\n')  # Split the ASCII art into individual lines for processing.
    start = x - len(dark)  # Calculate the starting position based on the number of lines in the ASCII art.
    step = 0  # Initialize color intensity step.

    # Loop to create a sliding effect from left to right.
    for i in range(0, y // 3, 3):
        util.clear()  # Clear the terminal before displaying the next frame.

        # Loop through each line of the ASCII art.
        for row, line in enumerate(dark):
            cursor = f"\033[{start + row};{i}H"  # Position the cursor for each line.
            sys.stdout.write(cursor + f'\033[32m' + util.fade_text(line, step, 0, step))  # Write the faded text to the terminal.

        sys.stdout.flush()  # Ensure that all output is written to the terminal.
        time.sleep(0.3)  # Delay to slow down the animation.
        step += 15  # Increase the intensity step for the next frame.

    # Final frame to ensure the text remains visible at the end of the animation.
    for row, line in enumerate(dark):
        cursor = f"\033[{start + row};{i}H"
        sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))


def morph():
    """
    Animate the 'morpheus' ASCII art with a fade in and fade out effect. This function gradually
    increases and then decreases the brightness of the text to create a pulsating visual effect.

    Utilizes ASCII escape codes to position and color the text within the terminal window.
    """
    # Split the 'morpheus' ASCII art into individual lines for processing.
    morpheus = util.morpheus.split('\n')
    
    step = 0  # Initialize the color intensity step.
    
    # Fade in effect: Gradually increase the color intensity from 0 to 240.
    while step <= 240:
        util.clear()  # Clear the terminal for a fresh frame.
        time.sleep(0.05)  # Short delay to slow down the animation.
        
        # Loop through each line of the ASCII art.
        for row, line in enumerate(morpheus):
            # Write each line with increasing color intensity to the terminal.
            sys.stdout.write(f"\033[{row + 1};1H" + util.fade_text(line, red=step, green=step, blue=step))
        
        sys.stdout.flush()  # Ensure that all output is written to the terminal.
        time.sleep(0.15)  # Delay to allow the fade effect to be noticeable.
        step += 20  # Increase the intensity for the next frame.

    # Fade out effect: Gradually decrease the color intensity from 240 back to 0.
    while step >= 0:
        util.clear()  # Clear the terminal for a fresh frame.
        time.sleep(0.05)  # Short delay to slow down the animation.
        
        # Loop through each line of the ASCII art.
        for row, line in enumerate(morpheus):

            # Write each line with decreasing color intensity to the terminal.
            sys.stdout.write(f"\033[{row + 1};1H" + util.fade_text(line, red=step, green=step, blue=step))
        
        sys.stdout.flush()  # Ensure that all output is written to the terminal.
        time.sleep(0.15)  # Delay to allow the fade effect to be noticeable.
        step -= 20  # Decrease the intensity for the next frame.

    util.clear()  # Clear the terminal once the animation is complete to prepare for the next screen.


class GUI:

    def __enter__(self):
        """
        Initialize the curses application interface. This method is automatically
        called when the GUI class is entered using a 'with' statement.

        It sets up the terminal for curses-based interactions by turning off
        echoing of input keys, enabling special key processing, and starting color support.

        Returns:
            self (GUI): Returns an instance of itself to be used within the 'with' block.
        """
        self.stdscr = curses.initscr()  # Initialize the window, returning a window object representing the whole screen.
        curses.noecho()  # Turn off automatic echoing of keys to the screen.
        curses.cbreak()  # React to keys instantly, without requiring the Enter key to be pressed.
        self.stdscr.keypad(True)  # Enable keypad mode.
        curses.start_color()  # Start color functionality.
        self.stdscr.clear()  # Clear the screen.

        self.MAX_X, self.MAX_Y = self.stdscr.getmaxyx()  # Get the maximum dimensions of the terminal.
        self.mid_x = self.MAX_X // 2  # Compute the middle of the screen horizontally.
        self.mid_y = self.MAX_Y // 2  # Compute the middle of the screen vertically.

        return self  # Return the GUI instance for use in the 'with' block.

    def __exit__(self, type, except_value, traceback):
        """
        Clean up the curses application interface. This method is automatically
        called when exiting a 'with' block where a GUI instance was used.

        It restores the terminal to its original state by disabling cbreak mode, re-enabling
        key echoing, and stopping curses. If there were any exceptions, it could be handled here.

        Args:
            type: The type of the exception if an exception was raised in the 'with' block.
            except_value: The value of the exception if an exception was raised.
            traceback: The traceback of the exception if an exception was raised.
        """
        self.stdscr.clear()  # Clear the screen one last time.
        curses.nocbreak()  # Switch back to the normal input mode.
        self.stdscr.keypad(False)  # Turn off keypad mode.
        curses.echo()  # Enable echoing of keys.
        curses.endwin()  # End curses mode and restore the original terminal state.

    @util.threaded
    def loading(self, end_thread, display='testing'):
        """
        Display a loading animation on the screen. This function runs in a separate thread to
        allow the animation to continue independently of other processes.

        Args:
            end_thread (threading.Event): An event to signal when the loading animation should stop.
            display (str): Text to display alongside the loading animation, defaulting to 'testing'.
        """

        ellipsis = '... '  # Characters used to create the visual effect of a loading animation.
        index = 0  # Initialize the index to control the movement of the ellipsis.
        curses.curs_set(0)  # Hide the cursor.

        mid_x = self.mid_x  # Retrieve the middle x-coordinate from the GUI instance.
        mid_y = self.mid_y  # Retrieve the middle y-coordinate from the GUI instance.

        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Set up color pair for the loading text.

        # Continuously display the loading animation until the end_thread event is set.
        while not end_thread.is_set():
            self.stdscr.clear()  # Clear the screen for a fresh frame of the animation.
            
            # Reset the ellipsis index if it reaches the end of the ellipsis string.
            if index == len(ellipsis):
                index = 0
            
            # Construct and display the loading message with ellipsis effect.
            self.stdscr.addstr(mid_x, mid_y - len(display) // 2, display + ellipsis[-index:], curses.color_pair(2))
            
            index += 1  # Move to the next character in the ellipsis string.
            self.stdscr.refresh()  # Refresh the screen to update the display.
            time.sleep(0.4)  # Introduce a short delay to control the speed of the animation.


    def connected(self):
        """
        Display a message indicating that a connection has been successfully established.
        This function updates the GUI to inform the user that the connection is ready.
        """
        curses.curs_set(0)  # Hide the cursor to improve display aesthetics.
        mid_x = self.mid_x  # Retrieve the middle x-coordinate of the screen from the GUI instance.
        mid_y = self.mid_y  # Retrieve the middle y-coordinate of the screen from the GUI instance.

        # Set up a color pair for displaying the connection message.
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        display = "[connection found]"  # Define the message to display.

        # Add the connection message to the screen. 
        # It is centered by adjusting the position based on the length of the message.
        self.stdscr.addstr(mid_x, mid_y - len(display) // 2, display, curses.color_pair(2))
        
        self.stdscr.refresh()  # Refresh the screen to update the display with the new message.
        time.sleep(3)  # Pause for 3 seconds to allow the user to read the message.


    def chat(self, curr_user):
        """
        Manage the chat interface, allowing users to send and receive messages.

        Args:
            curr_user (User): The current user instance which includes the user's socket.
        """

        curses.curs_set(0)  # Hide the cursor in the chat interface.  

        # Set up the dimensions for the chat and text entry interfaces.
        max_x = self.MAX_X - 2  # Calculate maximum X taking borders into account.
        max_y = self.MAX_Y - 2  # Calculate maximum Y taking borders into account.
        chat_max_height = max_x - 9  # Deduct space for the text entry window and padding.

        # Initialize color pairs for different elements in the chat interface.
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # For user's own messages.
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # For other messages.
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # For interface decorations.

        # Create windows for displaying chat messages and for user text input.
        chat_window = curses.newwin(max_x - 9, max_y - 4, 3, 4)  # Window for chat messages.
        text_entry_window = curses.newwin(3, max_y - 4, max_x - 3, 3)  # Window for user input.
        chat_window.scrollok(True)  # Enable scrolling of text within the window.

        # Draw interface boundaries using rectangles.
        self.stdscr.attron(curses.color_pair(3))
        rectangle(self.stdscr, 2, 2, max_x - 6, max_y)
        rectangle(self.stdscr, max_x - 4, 2, max_x, max_y)
        self.stdscr.attroff(curses.color_pair(3))
        self.stdscr.refresh()  # Refresh the screen to show the updated interface.

        messages = []  # List to store the chat messages.
        lock = threading.Lock()  # Lock for synchronizing access to the messages list.

        @util.threaded
        def receive_messages():
            """
            Continuously receive messages from the server or client and add them to the chat.
            """
            while True:
                try:
                    data = curr_user.socket.recv(1024).decode() # Receive data from the socket.
                    if not data:
                        break
                    with lock:
                        messages.append(f"{data}") # Append the received message to the list.
                        if len(messages) > chat_max_height - 1:
                            del messages[0] # Remove the oldest message to maintain window size.
                except Exception as e:
                    break
                    
        @util.threaded
        def display_messages():
            """
            Continuously update the chat window to display new messages.
            """
            while True:
                with lock:
                    chat_window.erase() # Clear the chat window for new messages.

                    # Calculate which messages to display based on the window height.
                    first_line_index = max(len(messages) - (chat_max_height - 1), 0)
                    for i, msg in enumerate(messages[first_line_index:]):
                        # Make sure not to try writing beyond the drawable area of the window
                        if i < chat_max_height - 1:
                            if msg[:len(curr_user)] == f'{curr_user}':
                                self.stdscr.attron(curses.color_pair(1))
                                chat_window.addstr(i, 0, msg)
                                self.stdscr.attroff(curses.color_pair(1))
                            else:
                                self.stdscr.attron(curses.color_pair(2))
                                chat_window.addstr(i, 0, msg)
                                self.stdscr.attroff(curses.color_pair(2))
                    chat_window.refresh()
                time.sleep(0.1) # Pause briefly before the next update.

        # Create a textbox for user message input.
        textbox = textpad.Textbox(text_entry_window, insert_mode=True)

        # Function to process input and append the user's message to the chat.
        def enter_message(x):
            """
            Define how the textbox handles input, using the 'Enter' key to submit a message.
            """
            if x == ord('\n'):
                return 7  # ASCII code for bell, used to terminate textbox.edit()
            else:
                return x
        
        # Start the threads for receiving and displaying messages.
        display_messages()
        receive_messages()

        # Main loop for handling user input and message sending.
        try:
            while True:
                text_entry_window.erase() # Clear the input window for new input.
                text_entry_window.refresh()
                textbox.stripspaces = True # Strip spaces from input.
                
                message = textbox.edit(enter_message).strip() # Get user input from textbox.
                message = f'{curr_user} {message}' # Format message with user identifier.

                if message:
                    with lock:
                        messages.append(message) # Add new message to messages list.
                        if len(messages) > chat_max_height - 1:
                            del messages[0] # Maintain chat window size by removing oldest messages.

                    text_entry_window.erase() # Clear the textbox after sending the message.
                    text_entry_window.refresh()

                    # Update the chat display after adding a new message.
                    with lock:
                        chat_window.erase()
                        for i, msg in enumerate(messages[-(chat_max_height - 1):]):
                            chat_window.addstr(i+1, 0, msg)
                        chat_window.refresh()

                    try:
                        curr_user.socket.sendall(message.encode()) # Send the message via the socket.
                    except Exception as e:
                        break # Exit the loop if sending fails.
                        
        finally:
            curr_user.socket.close() # Ensure the socket is closed when the chat ends.


    def login(self):
        """
        Handle the user login process with options to join as a client, host a session, or exit.
        Uses curses to handle user input and display options interactively.
        """
        curses.curs_set(0)  # Hide the cursor in the login interface.
        
        # Initialize color pairs for various elements.
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        # Display position constants.
        y, x = self.MAX_Y - 1, self.MAX_X - 1  # Get the last position coordinates of the screen.
        user_cursor = self.mid_y  # Starting cursor position in the middle of the screen.

        # Login instructions and options.
        guides = "[use arrow keys]"
        msg = "[join session]         [exit]         [host session]"
        self.stdscr.addstr(self.mid_x-1, self.mid_y - len(msg)//2, msg, curses.color_pair(2))  # Move the cursor to the new position
        self.stdscr.addstr(x-10, self.mid_y - len(guides)//2, guides)  # Move the cursor to the new position
        
        # Cursor display bar for selecting options.
        cursor_bar = "  "
        
        # Main loop to handle user input and navigation.
        while True:

            self.stdscr.refresh()  # Refresh the screen to reflect any changes.
            try:
                key = self.stdscr.getch()  # Capture user key press.
            except:
                key = None # Handle exception if key press fails.

            # Navigation and selection logic.
            if key == curses.KEY_LEFT and user_cursor >= self.mid_y:
                user_cursor -= 18 # Move cursor left.
            elif key == curses.KEY_RIGHT and user_cursor <= self.mid_y:
                user_cursor += 18 # Move cursor right.
            elif key == ord('\n') and user_cursor == self.mid_y - 18:
                return mk_client_user(), False # Option to join as a client.
            elif key == ord('\n') and user_cursor == self.mid_y + 18:
                return mk_host_user(), True # Option to host a session.
            elif key == ord('q'):
                break # Quit option.
            elif key == ord('\n') and user_cursor == self.mid_y:
                break # Execute the selected option.
            
            # Update display based on cursor position and selection.
            self.stdscr.clear()  # Clear the screen
            self.stdscr.addstr(self.mid_x, user_cursor-len(cursor_bar)//2, cursor_bar, curses.color_pair(1))
            self.stdscr.addstr(self.mid_x-1, self.mid_y - len(msg)//2, msg, curses.color_pair(2)) 
            self.stdscr.addstr(x-10, self.mid_y - len(guides)//2, guides)  
            self.stdscr.refresh()  # Refresh the screen

            # Definitions of helper functions to handle creating user instances.
            def mk_client_user():
                """
                Create a User instance for a client by collecting IP, port, and username.
                """
                curses.curs_set(1) # Make cursor visible for input.

                # Input fields and their setup.
                ip_text = '[IP address]'
                port_text = '[port number]'
                user_test = '[username]'
                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen

                # Define text input boxes and display them.
                # IP window
                self.stdscr.addstr(x-20, int(y*.3)+1, ip_text, curses.color_pair(2))
                rectangle(self.stdscr, x-19, int(y*.3), x-17, int(y*.6))
                ip_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
                ip_box = textpad.Textbox(ip_box_win)
                # Port window
                self.stdscr.addstr(x-16, int(y*.3)+1, port_text, curses.color_pair(2))
                rectangle(self.stdscr, x-15, int(y*.3), x-13, int(y*.6))
                port_box_win = curses.newwin(1, int(y*.3), x-14, int(y*.3)+1)
                port_box = textpad.Textbox(port_box_win)
                # Username window
                self.stdscr.addstr(x-12, int(y*.3)+1, user_test, curses.color_pair(2))
                rectangle(self.stdscr, x-11, int(y*.3), x-9, int(y*.6))
                user_box_win = curses.newwin(1, int(y*.3), x-10, int(y*.3)+1)
                user_box = textpad.Textbox(user_box_win)
                self.stdscr.refresh()

                # Collect user inputs.
                try:
                    ip = ip_box.edit().strip()
                    port = int(port_box.edit().strip())
                    username = user_box.edit().strip()
                except ValueError as e:
                    GUI.Error.display(self, f'{e}') # Display error and re-initiate login.
                    return self.login()

                curses.curs_set(0)
                self.stdscr.clear()
                self.stdscr.refresh()  # Refresh the screen
                return User(ip, port, username)

            def mk_host_user():
                """
                Create a User instance for hosting a session by collecting only the username.
                """
                curses.curs_set(1) # Make cursor visible for input.
                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen
                user_test = '[username]'

                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen

                # Define text input boxes and display them.
                # Username window
                self.stdscr.addstr(x-20, int(y*.3)+1, user_test, curses.color_pair(2))
                rectangle(self.stdscr, x-19, int(y*.3), x-17, int(y*.6))
                user_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
                user_box = textpad.Textbox(user_box_win)
                self.stdscr.refresh()

                # Collect username.
                username = user_box.edit().strip()
                curses.curs_set(0)
                self.stdscr.clear()
                self.stdscr.refresh()  # Refresh the screen

                return User(username = username)

    class Error(Exception):
        """
        A custom exception class for handling errors within the GUI. This class extends the standard
        Exception class and adds a method to display errors visually in the GUI.
        """
        def display(self, message):
            """
            Display an error message in the GUI.

            Args:
                message (str): The error message to be displayed to the user.
            """
            # Set up a color pair for displaying error messages.
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.curs_set(0) # Hide the cursor when displaying the error.

            self.stdscr.clear()  # Clear the screen before displaying anything.
            temp = ''  # Temporary string to build the error animation.
            error = 'error...'  # Placeholder text for the initial part of the error animation.
            index = 0  # Initialize an index to iterate over the error string.

            # Animate the display of 'error...' by adding one character at a time.
            while len(temp) != len(error):
                temp += error[index]  # Add the next character to temp.
                index += 1  # Increment the index.

                # Display the temporary string centered horizontally on the screen.
                self.stdscr.addstr(self.mid_x-1, self.mid_y-len(error)//2, temp, curses.color_pair(3))
                self.stdscr.refresh() # Refresh the screen to update the display.
                time.sleep(.1) # Pause between character updates for a typing effect.

            time.sleep(1) # Wait a moment before displaying the full error message.

            # Display the full error message below the 'error...' text.
            self.stdscr.addstr(self.mid_x+1, self.mid_y-len(message)//2, message, curses.color_pair(3))
            self.stdscr.refresh() # Refresh the screen to show the message.
            time.sleep(4) # Display the error message for 4 seconds.

            # Clear the screen and prompt the user to try again.
            self.stdscr.clear()  # Clear the screen
            self.stdscr.addstr(self.mid_x-2, self.mid_y-4, "Try again...", curses.color_pair(3))
            self.stdscr.refresh()  # Refresh the screen after displaying the prompt.
            time.sleep(2) # Wait for 2 seconds before clearing the screen.
            self.stdscr.clear()  # Finally, clear the screen to continue with other operations.
