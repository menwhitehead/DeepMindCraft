import SocketServer
import socket
from main import *
from game_config import *

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # Count of total actions performed by bot
        action_count = 0
        
        # Turn off TCP delays
        self.request.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        
        while True:
            # self.request is the TCP socket connected to the client
            incoming_mess = self.request.recv(16).strip()
            #print "Chosen action:", chosen_action

            if incoming_mess == "RESET":
                # Reset and start a new game
                print("\tGAME OVER.  SCORE: %d" % window.player.total_score)
                window.reset()
                step(window)  # update's the window's current_frame
            else:
                # perform the last chosen action
                window.player.doAction(incoming_mess)
                step(window)  # update's the window's current_frame
                
            # Set the last byte to be the previous reward
            window.current_frame[-2] = window.player.previous_reward
            window.current_frame[-1] = window.game_over

            
            # Send the bytes of the current frame
            self.request.sendall(window.current_frame)
            
            action_count += 1
            if action_count % COUNTER_DISPLAY_FREQUENCY == 0:
                print("TOTAL ACTION COUNT: %d" % action_count)


if __name__ == '__main__':
    global window

    # Verify the necessary directories exist and conform to the configurations in this file
    verify_directories()
    # Verify the necessary files conform to the configurations in this file
    verify_files()
    
    window = main()

    HOST, PORT = TCP_HOST, TCP_PORT

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
