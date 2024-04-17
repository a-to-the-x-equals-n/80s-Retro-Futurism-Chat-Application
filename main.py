import util
from threading import Event
from gui import GUI, morph, welcome_screen
import logging


# Set up logging to capture all debug information in an external log file.
logging.basicConfig(filename = 'app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# tail -f app.log

def main():
    """
    Main function to initialize and run the chat application.
    This function sets up the environment, handles user role selection, and manages the application lifecycle.
    """
    # Get the terminal size to properly configure the GUI.
    x,y = util.terminal_size()
    
    # Display the welcome screen with animations.
    welcome_screen(x,y)

    # Display additional animations after the welcome screen.
    morph()

    # Use the GUI class as a context manager.
    # Allow the user to log in and choose their role (host or client).
    with GUI() as gui:
        curr_user, hosting = gui.login()

    user = ''
    try:
        if hosting:
            user = "HOST"
            logging.info("HOST: Starting server...")
            curr_user.listening() # Host starts listening for incoming connections.
             
            with GUI() as gui:
                kill_thread = Event()
                load_thread = gui.loading(kill_thread, 'listening') # Show loading animation.
                logging.info("HOST: Server is listening for connections...")

                # Accept an incoming connection once available.
                online = True
                while online:
                    client_conn, client_addr = curr_user.socket.accept()
                    logging.info(f"HOST: Connected to {client_addr}")
                    curr_user.socket = client_conn # Update the socket to the connected client.
                    online = False

                # End the loading animation once the connection is established.
                kill_thread.set()
                load_thread.join()
    
        else:
            user = 'CLIENT'
            logging.info("CLIENT: Searching for server...")
            server = curr_user.searching() # Client searches for the server.

            with GUI() as gui:
                kill_thread = Event()
                load_thread = gui.loading(kill_thread, 'searching') # Show loading animation.

                logging.info(f"CLIENT: Connecting to server at {server}...")
                curr_user.socket.connect(server) # Connect to the server.

                logging.info("CLIENT: Connected to server.")

                # End the loading animation once the connection is established.
                kill_thread.set()
                load_thread.join()

    except Exception as e:
        logging.error(F"{user}: An error occurred: {e}", exc_info=True)
        logging.info(F"{user}: An error occurred: {e}")
        kill_thread.set()
        load_thread.join()
        curr_user.socket.close() # Ensure the socket is closed on error.
        logging.info(f"{user}: Socket closed.")

    # After successful connection, start the chat interface.
    with GUI() as gui:
        gui.connected() # Show connection successful message.
        gui.chat(curr_user) # Enter the chat interface.

    # Close the socket and log the closure once the chat session ends.
    curr_user.socket.close()
    logging.info(f"{user}: Socket closed.")

if __name__ == "__main__": 
    main() # Execute the main function if the script is run directly.