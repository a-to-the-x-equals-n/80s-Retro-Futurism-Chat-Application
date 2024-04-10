import time
import util
import sys
from user import User
from login_interface import login
from chat_interface import chat
import curses


def main():
    
    """
    Main function to initialize the program.
    """
    x,y = util.terminal_size()
    
    welcome_screen(x,y)
    sys.stdout.flush()
    util.clear()
    morph()

    stdscr, connection, host_user = curses.wrapper(login)
    
    temp = ''
    listen = 'listening...'
    index = 0
    curses.curs_set(0)

    MAX_X, MAX_Y = stdscr.getmaxyx()
    mid_x = MAX_X//2 # 28
    mid_y = MAX_Y//2 # 118
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    while not connection.is_set():
        
        if index >= len(listen):
            index = 0
        temp += listen[index]  # Add the next letter to temp
        index += 1  # Move to the next letter
        stdscr.addstr(mid_x, mid_y-3, temp, curses.color_pair(3))
        time.sleep(.3)


    # Transition to the chat interface
    curses.wrapper(lambda stdscr: chat(stdscr, host_user))




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


if __name__ == "__main__": 
    main()