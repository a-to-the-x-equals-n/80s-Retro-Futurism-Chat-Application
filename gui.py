import curses
import util
import time
from curses import textpad
from curses.textpad import rectangle
import threading
from user import User
import sys
from threading import Event


def welcome_screen(x,y):
    """
    Initialize the screen with animated text effects.

    Args:
        x (int): The number of rows in the terminal.
        y (int): The number of columns in the terminal.
    """
    tunnel_thread = tunnel(x//2,y)
    dark_thread = dark(x//2,y)

    tunnel_thread.join()
    dark_thread.join()


    dark_tunnel_display = []
    dark_tunnel_display.extend(util.dark.split('\n'))
    dark_tunnel_display.extend(util.tunnel.split('\n'))

   
    start = x//2-6
    step = 0
    while step < 255:
        util.clear()
        sys.stdout.flush()  # Flush the buffer to ensure immediate printing
        for row, line in enumerate(dark_tunnel_display):
            cursor = f"\033[{start+row};{39}H"
            sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))
        time.sleep(0.2)
        step+=30
        sys.stdout.write(f"\033[{x//2};{y//2-10}H" + util.fade_text(f"-[PRESS ENTER]-", red = 0, green = step, blue = step//2))

    sys.stdout.write(f"\033[{x//2};{y//2-10}H" + util.fade_text(f"-[PRESS ENTER]-", red = 0, green = 255, blue = step//2))

    
    # Wait for user to press `Enter`
    input()

@util.threaded
def tunnel(x, y):
    """
    Function to animate 'tunnel' text.

    Args:
        x (int): The starting row position.
        y (int): The starting column position.
    """
    tunnel = util.tunnel.split('\n')
    start = x
    step = 0
    for i in range(0, y//3, 3):
        util.clear()
        # ANSI escape codes to move cursor to specified row and column

        #   {row} {col}
        for row, line in enumerate(tunnel):
            cursor = f"\033[{start+row};{y-42-i}H"
            sys.stdout.write(cursor + util.fade_text(line, step, 0, step))
        
        sys.stdout.flush()  # Flush the buffer to ensure immediate printing
        time.sleep(0.3)
        step+=15
    for row, line in enumerate(tunnel):
            cursor = f"\033[{start+row};{y-42-i}H"
            sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))

@util.threaded
def dark(x, y):
    """
    Function to animate 'dark' text.

    Args:
        x (int): The starting row position.
        y (int): The starting column position.
    """
    dark = util.dark.split('\n')    
    start = x-len(dark)
    step = 0
    for i in range(0,y//3,3):
        util.clear()
        for row, line in enumerate(dark):
            cursor = f"\033[{start+row};{i}H"
            sys.stdout.write(cursor + f'\033[32m' + util.fade_text(line, step, 0, step))

        sys.stdout.flush()  # Flush the buffer to ensure immediate printing
        time.sleep(0.3)
        step+=15
    for row, line in enumerate(dark):
            cursor = f"\033[{start+row};{i}H"
            sys.stdout.write(cursor + util.fade_text(line, 215, 0, 255))


def morph():
    morpheus = util.morpheus.split('\n')
    step = 0
    while step <= 240:
        util.clear()
        time.sleep(.05)
        for row, line in enumerate(morpheus):
            sys.stdout.write(f"\033[{row + 1};1H" + util.fade_text(line, red=step, green=step, blue=step))
        sys.stdout.flush()
        time.sleep(0.15)
        step += 20

    # After it fades in, let it fade out
    while step >= 0:
        util.clear()
        time.sleep(.05)
        for row, line in enumerate(morpheus):
            sys.stdout.write(f"\033[{row + 1};1H" + util.fade_text(line, red=step, green=step, blue=step))
        sys.stdout.flush()
        time.sleep(0.15)
        step -= 20

    util.clear()

class GUI:

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.start_color()
        self.stdscr.clear()

        self.MAX_X, self.MAX_Y = self.stdscr.getmaxyx()
        self.mid_x = self.MAX_X//2
        self.mid_y = self.MAX_Y//2

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        # if exc_type is not None:
        self.stdscr.keypad(False)
        curses.echo()
        self.stdscr.clear()
        curses.endwin()

    @util.threaded
    def loading(self, end_thread, display = 'testing'):

        ellipsis = '... '
        index = 0
        curses.curs_set(0)

        mid_x = self.mid_x
        mid_y = self.mid_y
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        while not end_thread.is_set():
            self.stdscr.clear()  # Clear the screen
            if index == len(ellipsis):
                index = 0
            self.stdscr.addstr(mid_x, mid_y-len(display)//2, display + ellipsis[-index:], curses.color_pair(2))
            index += 1  # Move to the next letter
            self.stdscr.refresh()  # Refresh the screen
            time.sleep(.4)

    def connected(self):
        curses.curs_set(0)
        mid_x = self.mid_x
        mid_y = self.mid_y
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        display = "[connection found]"
        self.stdscr.addstr(mid_x, mid_y-len(display)//2, display, curses.color_pair(2))
        self.stdscr.refresh()  # Refresh the screen
        time.sleep(3)

    def chat(self, curr_user):

        curses.curs_set(0)  

        # Set up the chat interface
        max_x = self.MAX_X - 2
        max_y = self.MAX_Y - 2
        chat_max_height = max_x - 9

        # color pairs
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        # Create windows for the top and bottom halves
        chat_window = curses.newwin(max_x-9, max_y-4, 3, 4)
        text_entry_window = curses.newwin(3, max_y-4, max_x-3, 3)
        chat_window.scrollok(True)

        # Draw rectangles for interface boundaries
        self.stdscr.attron(curses.color_pair(3))
        rectangle(self.stdscr, 2, 2, max_x-6, max_y)
        rectangle(self.stdscr, max_x - 4, 2, max_x, max_y)
        self.stdscr.attroff(curses.color_pair(3))
        self.stdscr.refresh()

        messages = []
        lock = threading.Lock()

        @util.threaded
        def receive_messages():
            while True:
                try:
                    data = curr_user.socket.recv(1024).decode()
                    if not data:
                        break
                    with lock:
                        messages.append(f"{data}")
                        if len(messages) > chat_max_height - 1:
                            del messages[0]
                except Exception as e:
                    break
                    
        @util.threaded
        def display_messages():
            while True:
                with lock:
                    chat_window.erase()

                    # Calculate the index of the first message to display based on the window height
                    first_line_index = max(len(messages) - (chat_max_height - 1), 0)
                    # Display messages starting from the first_line_index
                    for i, msg in enumerate(messages[first_line_index:]):
                        # Make sure not to try writing beyond the drawable area of the window
                        if i < chat_max_height - 1:
                            if msg[:len(curr_user)] == f'{curr_user}':
                                self.stdscr.attron(curses.color_pair(1))
                                chat_window.addstr(i, 0, msg)
                                self.stdscr.attroff(curses.color_pair(1))
                            self.stdscr.attron(curses.color_pair(2))
                            chat_window.addstr(i, 0, msg)
                            self.stdscr.attroff(curses.color_pair(2))
                    chat_window.refresh()
                time.sleep(0.1)

        # Create a textbox for input
        textbox = textpad.Textbox(text_entry_window, insert_mode=True)

        # Function to accept user input and append it to messages
        def enter_message(x):
            if x == ord('\n'):
                return 7  # ASCII code for bell, used to terminate textbox.edit()
            else:
                return x
        
        display_messages()
        receive_messages()

        # Display messages in the chat window
        try:
            while True:

                # Clear bottom window and get user input
                text_entry_window.erase()
                text_entry_window.refresh()
                textbox.stripspaces = True
                
                message = textbox.edit(enter_message).strip()
                message = f'{curr_user} {message}'

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
                        for i, msg in enumerate(messages[-(chat_max_height - 1):]):
                            chat_window.addstr(i+1, 0, msg)
                        chat_window.refresh()

                    try:
                        curr_user.socket.sendall(message.encode())
                    except Exception as e:
                        break
                        


                    #     for i, msg in enumerate(messages):
                    #         if msg[:len(curr_user)] == f'{curr_user}':
                    #             self.stdscr.attron(curses.color_pair(1))
                    #             chat_window.addstr(i, 0, msg)
                    #             self.stdscr.attroff(curses.color_pair(1))
                    #         self.stdscr.attron(curses.color_pair(2))
                    #         chat_window.addstr(i, 0, msg)
                    #         self.stdscr.attroff(curses.color_pair(2))
                    #     chat_window.refresh()

                    # if not recv_thread.is_alive() and not send_thread.is_alive():
                    #     break
        finally:
            # recv_thread.join()
            # send_thread.join()
            curr_user.socket.close()


    def login(self):

        curses.curs_set(0)  # Make cursor visible
        # self.stdscr.keypad(True)  # Enable keypad mode
        
        
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        

        y, x = self.MAX_Y - 1, self.MAX_X-1  # Starting position of the cursor
        user_cursor = self.mid_y


        guides = "[use arrow keys]"
        msg = "[join session]         [exit]         [host session]"
        
        self.stdscr.addstr(self.mid_x-1, self.mid_y - len(msg)//2, msg, curses.color_pair(2))  # Move the cursor to the new position
        self.stdscr.addstr(x-10, self.mid_y - len(guides)//2, guides)  # Move the cursor to the new position
        
        cursor_bar = "  "
        
        while True:

            self.stdscr.refresh()  # Refresh the screen
            try:
                key = self.stdscr.getch()  # Get user input
            except:
                key = None

            if key == curses.KEY_LEFT and user_cursor >= self.mid_y:
                user_cursor -= 18
            elif key == curses.KEY_RIGHT and user_cursor <= self.mid_y:
                user_cursor += 18

            elif key == ord('\n') and user_cursor == self.mid_y - 18:
                
                return mk_client_user(), False

            
            elif key == ord('\n') and user_cursor == self.mid_y + 18:
                
                return mk_host_user(), True
            
            elif key == ord('q'):
                break
            elif key == ord('\n') and user_cursor == self.mid_y:
                break
            

            self.stdscr.clear()  # Clear the screen
            self.stdscr.addstr(self.mid_x, user_cursor-len(cursor_bar)//2, cursor_bar, curses.color_pair(1))  # Move the cursor to the new position
            self.stdscr.addstr(self.mid_x-1, self.mid_y - len(msg)//2, msg, curses.color_pair(2))  # Move the cursor to the new position
            self.stdscr.addstr(x-10, self.mid_y - len(guides)//2, guides)  # Move the cursor to the new position
            self.stdscr.refresh()  # Refresh the screen


            def mk_client_user():

                curses.curs_set(1)
                ip_text = '[IP address]'
                port_text = '[port number]'
                user_test = '[username]'

                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen


                self.stdscr.addstr(x-20, int(y*.3)+1, ip_text, curses.color_pair(2))
                rectangle(self.stdscr, x-19, int(y*.3), x-17, int(y*.6))
                ip_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
                ip_box = textpad.Textbox(ip_box_win)
                

                self.stdscr.addstr(x-16, int(y*.3)+1, port_text, curses.color_pair(2))
                rectangle(self.stdscr, x-15, int(y*.3), x-13, int(y*.6))
                port_box_win = curses.newwin(1, int(y*.3), x-14, int(y*.3)+1)
                port_box = textpad.Textbox(port_box_win)
                

                self.stdscr.addstr(x-12, int(y*.3)+1, user_test, curses.color_pair(2))
                rectangle(self.stdscr, x-11, int(y*.3), x-9, int(y*.6))
                user_box_win = curses.newwin(1, int(y*.3), x-10, int(y*.3)+1)
                user_box = textpad.Textbox(user_box_win)
                self.stdscr.refresh()

                try:
                    # Get input from the user
                    ip = ip_box.edit().strip()
                    port = int(port_box.edit().strip())
                    username = user_box.edit().strip()

                except ValueError as e:
                    GUI.Error.display(self, f'{e}')
                    return self.login()

                curses.curs_set(0)
                self.stdscr.clear()
                self.stdscr.refresh()  # Refresh the screen

                user = User(ip, port, username)
                return user

            def mk_host_user():

                curses.curs_set(1)
                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen
                user_test = '[username]'

                self.stdscr.clear()  # Clear the screen
                self.stdscr.refresh()  # Refresh the screen

                self.stdscr.addstr(x-20, int(y*.3)+1, user_test, curses.color_pair(2))
                rectangle(self.stdscr, x-19, int(y*.3), x-17, int(y*.6))
                user_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
                user_box = textpad.Textbox(user_box_win)
                
                self.stdscr.refresh()

                username = user_box.edit().strip()
                curses.curs_set(0)
                self.stdscr.clear()
                self.stdscr.refresh()  # Refresh the screen

                user = User(username = username)

                return user

    class Error(Exception):
        def display(self, message):
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.curs_set(0)
            self.stdscr.clear()
            temp = ''
            error = 'error...'
            index = 0
            while len(temp) != len(error):
                temp += error[index]  # Add the next letter to temp
                index += 1  # Move to the next letter
                self.stdscr.addstr(self.mid_x-1, self.mid_y-len(error)//2, temp, curses.color_pair(3))
                self.stdscr.refresh()
                time.sleep(.1)

            time.sleep(1)
            self.stdscr.addstr(self.mid_x+1, self.mid_y-len(message)//2, message, curses.color_pair(3))
            self.stdscr.refresh()
            time.sleep(4)

            self.stdscr.clear()  # Clear the screen
            self.stdscr.addstr(self.mid_x-2, self.mid_y-4, "Try again...", curses.color_pair(3))
            self.stdscr.refresh()  # Refresh the screen
            time.sleep(2)
            self.stdscr.clear()  # Clear the screen


       



'''

if __name__ == "__main__":
    with GUI() as gui:
        gui.main_loop()

'''
