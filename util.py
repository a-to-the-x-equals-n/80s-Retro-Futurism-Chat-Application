import time
import os
import threading
import shutil


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target = func, args = args, kwargs = kwargs)
        thread.start()
        return thread
    return wrapper

# @threaded
# def task1():
#     print("Executing task 1...")
# @threaded
# def task2():
#     print("Executing task 2...")
# thread1.join()
# thread2.join()


# def terminal_size():

#     # Initialize curses
#     stdscr = curses.initscr()
#     # Get terminal size
#     y, x = stdscr.getmaxyx()
#     # Clean up curses
#     curses.endwin()
    
#     return y, x


def terminal_size():
    columns, rows = shutil.get_terminal_size()
    return rows, columns  # Return rows first, then columns

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')


# Function to print faded text
def fade_out(text):
    color_intensity = 255  # Initial color intensity
    step = 50  # Step size for color reduction
    
    # Loop until color_intensity reaches a value where text becomes invisible
    while color_intensity >= -step:
        # Construct a string with text color intensity
        if color_intensity >= 0:
            faded_text = f"\033[38;2;{color_intensity};{color_intensity};{color_intensity}m{text}\033[0m"
        else:
            faded_text = " " * len(text)  # Print spaces when text is invisible
        # Print faded text
        print(faded_text)
        # Reduce color intensity
        color_intensity -= step
        # Wait for a short duration for fading effect
        time.sleep(0.27)
        os.system('clear')

def fade_in(text):
    color_intensity = 0  # Initial color intensity
    step = 50  # Step size for color reduction
    
    # Loop until color_intensity reaches a value where text becomes invisible
    while color_intensity <= 255:
        # Construct a string with text color intensity
        if color_intensity >= 0:
            faded_text = f"\033[38;2;{color_intensity};{color_intensity};{color_intensity}m{text}\033[0m"
        else:
            faded_text = " " * len(text)  # Print spaces when text is invisible
        # Print faded text
        print(faded_text)
        # Reduce color intensity
        color_intensity += step
        # Wait for a short duration for fading effect
        time.sleep(0.27)
        

def fade_text(text, red = 0, green = 0, blue = 0):
    # Construct a string with text color intensity
    color_intensity = (red + green + blue) / 3
    if color_intensity > 0:
        faded_text = f"\033[38;2;{red};{green};{blue}m{text}\033[0m"
    else:
        faded_text = " " * len(text)  # Print spaces when text is invisible
    # Print faded text
    return(faded_text)

    

# Welcome Screen
dark = '''      ______   ___  ______  _   __
      |  _  \ / _ \ | ___ \| | / /
      | | | |/ /_\ \| |_/ /| |/ / 
      | | | ||  _  ||    / |    \ 
      | |/ / | | | || |\ \ | |\  \\
      |___/  \_| |_/\_| \_|\_| \_/'''
tunnel = ''' _____  _   _  _   _  _   _  _____  _     
|_   _|| | | || \ | || \ | ||  ___|| |    
  | |  | | | ||  \| ||  \| || |__  | |    
  | |  | | | || . ` || . ` ||  __| | |    
  | |  | |_| || |\  || |\  || |___ | |____
  \_/   \___/ \_| \_/\_| \_/\____/ \_____/'''


if __name__ == "__main__":
    fade_text(dark+tunnel)
