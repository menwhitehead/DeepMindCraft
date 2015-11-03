import SocketServer
import socket
from main import *
from game_globals import *

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

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
                print("\tGAME SCORE: %d" % window.player.total_score)
                window.reset()
                step(window)  # update's the window's current_frame
            else:
                # perform the last chosen action
                window.player.doAction(incoming_mess)
                step(window)  # update's the window's current_frame
                
            # Build and send a new message
            # Message contains all the bytes of the current game frame
            # Last value in the message is the previous action's reward
            mess = ''
            #for i in window.current_frame:
            for pix in window.current_frame:
                mess += "%d," % pix

            self.request.sendall(mess + str(window.player.previous_reward) + "\n")  # send one combined message

            action_count += 1
            if action_count % COUNTER_DISPLAY_FREQUENCY == 0:
                print("ACTION COUNT: %d" % action_count)


if __name__ == '__main__':
    global window
    window = main()

    HOST, PORT = TCP_HOST, TCP_PORT

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
