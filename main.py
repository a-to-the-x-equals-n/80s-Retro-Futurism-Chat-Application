import time
import util
import sys


def main():

    x,y = util.terminal_size()
    
    init_screen(x,y)
    


def init_screen(x,y):
    tunnel_thread = tunnel(x//2,y)
    dark_thread = dark(x//2,y)

    tunnel_thread.join()
    dark_thread.join()

    time.sleep(0.2)
    sys.stdout.write(f"\033[{x//2+10};{y//2-6}H" + util.fade_text(f"-[ENTER]-", 0, 255, 100))
        
    input()



@util.threaded
def tunnel(x, y):

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