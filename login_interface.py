import curses
from curses import textpad
from curses.textpad import rectangle
import util
import time
import threading
from user import User

def login(stdscr):

    curses.curs_set(0)  # Make cursor visible
    stdscr.keypad(True)  # Enable keypad mode
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)


    MAX_X, MAX_Y = stdscr.getmaxyx()
    y, x = MAX_Y - 1, MAX_X-1  # Starting position of the cursor
    user_cursor = mid_y = y//2
    mid_x = x//2

    guides = "[use arrow keys]"
    msg = "[find session]         [exit]         [listen for session]"
    # stdscr.clear()  # Clear the screen
    stdscr.addstr(mid_x-1, mid_y - len(msg)//2+2, msg, curses.color_pair(2))  # Move the cursor to the new position
    stdscr.addstr(x-10, mid_y - len(guides)//2-1, guides)  # Move the cursor to the new position
    # stdscr.refresh()  # Refresh the screen
    cursor_bar = "  "
     
    while True:

        stdscr.refresh()  # Refresh the screen
        try:
            key = stdscr.getch()  # Get user input
        except:
            key = None

        if key == curses.KEY_LEFT and user_cursor >= mid_y:
            user_cursor -= 20
        elif key == curses.KEY_RIGHT and user_cursor <= mid_y:
            user_cursor += 20

        elif key == ord('\n') and user_cursor == mid_y - 20:
            client_user = find_session()
            return client_user
        
        elif key == ord('\n') and user_cursor == mid_y + 20:
            connection, host_user = set_listening()
            return stdscr, connection, host_user
        
        elif key == ord('q'):
            break
        elif key == ord('\n') and user_cursor == mid_y:
            break
        

        stdscr.clear()  # Clear the screen
        stdscr.addstr(mid_x, user_cursor-len(cursor_bar)//2, cursor_bar, curses.color_pair(1))  # Move the cursor to the new position
        stdscr.addstr(mid_x-1, mid_y - len(msg)//2+2, msg, curses.color_pair(2))  # Move the cursor to the new position
        stdscr.addstr(x-10, mid_y - len(guides)//2-1, guides)  # Move the cursor to the new position
        stdscr.refresh()  # Refresh the screen


        def find_session():

            curses.curs_set(1)
            ip_text = '[IP address]'
            port_text = '[port numer]'
            user_test = '[username]'

            stdscr.clear()  # Clear the screen
            stdscr.refresh()  # Refresh the screen


            stdscr.addstr(x-20, int(y*.3)+1, ip_text, curses.color_pair(2))
            rectangle(stdscr, x-19, int(y*.3), x-17, int(y*.6))
            ip_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
            ip_box = textpad.Textbox(ip_box_win)
            

            stdscr.addstr(x-16, int(y*.3)+1, port_text, curses.color_pair(2))
            rectangle(stdscr, x-15, int(y*.3), x-13, int(y*.6))
            port_box_win = curses.newwin(1, int(y*.3), x-14, int(y*.3)+1)
            port_box = textpad.Textbox(port_box_win)
            

            stdscr.addstr(x-12, int(y*.3)+1, user_test, curses.color_pair(2))
            rectangle(stdscr, x-11, int(y*.3), x-9, int(y*.6))
            user_box_win = curses.newwin(1, int(y*.3), x-10, int(y*.3)+1)
            user_box = textpad.Textbox(user_box_win)
            stdscr.refresh()

            try:
                
                # Get input from the user
                ip = ip_box.edit().strip()
                port = int(port_box.edit().strip())
                username = user_box.edit().strip()
            except ValueError:
                curses.curs_set(0)
                stdscr.clear()
                temp = ''
                error = 'error...'
                index = 0
                while len(temp) != len(error):
                    temp += error[index]  # Add the next letter to temp
                    index += 1  # Move to the next letter
                    stdscr.addstr(mid_x, mid_y-3, temp, curses.color_pair(3))
                    stdscr.refresh()
                    time.sleep(.3)
                
                time.sleep(1)
                stdscr.addstr(mid_x+2, mid_y-13, "invalid assignment operation", curses.color_pair(3))
                stdscr.refresh()

                time.sleep(2)
                stdscr.clear()  # Clear the screen
                stdscr.addstr(mid_x+2, mid_y-5, "Try again...", curses.color_pair(4))
                stdscr.refresh()  # Refresh the screen
                time.sleep(2)

                find_session()

            curses.curs_set(0)
            stdscr.clear()
            stdscr.refresh()  # Refresh the screen

            user = User(ip, port, username)
            return user

        def set_listening():

            curses.curs_set(1)
            stdscr.clear()  # Clear the screen
            stdscr.refresh()  # Refresh the screen
            user_test = '[username]'

            stdscr.clear()  # Clear the screen
            stdscr.refresh()  # Refresh the screen


            stdscr.addstr(x-20, int(y*.3)+1, user_test, curses.color_pair(2))
            rectangle(stdscr, x-19, int(y*.3), x-17, int(y*.6))
            user_box_win = curses.newwin(1, int(y*.3), x-18, int(y*.3)+1)
            user_box = textpad.Textbox(user_box_win)
            
            stdscr.refresh()

            username = user_box.edit().strip()
            curses.curs_set(0)
            stdscr.clear()
            stdscr.refresh()  # Refresh the screen

            user = User(username = username)
            connection_made = threading.Event()
            user.start_server(connection_made)
            return connection_made, user

            






if __name__ == "__main__": 
    curses.wrapper(login)