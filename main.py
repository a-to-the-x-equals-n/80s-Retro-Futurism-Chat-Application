import util
from threading import Event
from user import User
import curses
from gui import GUI, morph, welcome_screen
import logging

logging.basicConfig(filename = 'app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    
    """
    Main function to initialize the program.
    """
    # x,y = util.terminal_size()
    
    # welcome_screen(x,y)

    # morph()

    with GUI() as gui:
        curr_user, hosting = gui.login()

    user = ''
    try:
        if hosting:
            user = "HOST"
            logging.info("HOST: Starting server...")
            curr_user.listening()
            with GUI() as gui:
                kill_thread = Event()
                load_thread = gui.loading(kill_thread, 'listening')
                logging.info("HOST: Server is listening for connections...")
                online = True
                while online:
                    client_conn, client_addr = curr_user.socket.accept()
                    logging.info(f"HOST: Connected to {client_addr}")
                    curr_user.socket = client_conn
                    online = False
                kill_thread.set()
                load_thread.join()
    
        else:
            user = 'CLIENT'
            logging.info("CLIENT: Searching for server...")
            server = curr_user.searching()
            with GUI() as gui:
                kill_thread = Event()
                load_thread = gui.loading(kill_thread, 'searching')

                logging.info(f"CLIENT: Connecting to server at {server}...")

                curr_user.socket.connect(server)

                logging.info("CLIENT: Connected to server.")

                kill_thread.set()
                load_thread.join()
    except Exception as e:
        logging.error(F"{user}: An error occurred: {e}", exc_info=True)
        logging.info(F"{user}: An error occurred: {e}")
        kill_thread.set()
        load_thread.join()
        curr_user.socket.close()
        logging.info(f"{user}: Socket closed.")


    with GUI() as gui:
        gui.connected()

    with GUI() as gui:
        gui.chat(curr_user)


    curr_user.socket.close()
    logging.info(f"{user}: Socket closed.")

    # Transition to the chat interface
    # T0D0: transition to chat


if __name__ == "__main__": 
    main()