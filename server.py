from connection import Connection
import select
import socket

class SocketServer(Connection):
    # Set server u
    LISTENMODE=5
    def __init__(self,ip,port,listen_mode):
        super().__init__(ip,port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_mode=SocketServer.LISTENMODE
        self.active_connections = [self.socket]



    # Start the server
    def start(self):
        try:
            print("[STARTING SERVER]")
            #bind the ip and port to the socket
            self.socket.bind((self.ip,self.port))
            #set listening mode
            self.socket.listen(self.listen_mode)
            while True:

                # Calls Unix select() system call or Windows select() WinSock call with three parameters:
                #   - rlist - sockets to be monitored for incoming data
                #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
                #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
                # Returns lists:
                #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
                #   - writing - sockets ready for data to be send thru them
                #   - errors  - sockets with some exceptions
                # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
                print(f"[WATING FOR DATA OR CONNECTIONS]")
                read_sockets, _, exception_sockets = select.select(self.active_connections, [], self.active_connections)

                # Iterate over notified sockets
                for notified_socket in read_sockets:

                    # If notified socket is a server socket - new connection, accept it
                    if notified_socket == self.socket:

                        # Accept new connection
                        # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                        # The other returned object is ip/port set
                        client_socket, client_address = self.socket.accept()

                        client_ip = client_address[0]
                        client_port = client_address[1]
                        print(f"[ACCEPTED CONNECTION] {client_ip}:{client_port}")

                        # Add accepted socket to active connections
                        #add the new connection
                        self.active_connections.append(client_socket)

                        # Broadcast message to all active connections

                        self.send("Welcome to the server", client_socket)

                    # Else existing socket is sending a message
                    else:

                        # Receive message
                        message = self.receive(notified_socket)
                        print(message)

                        # If client wants to exit, close connection, cleanup
                        if message == "[REFRESH]":
                            self.send("Refreshed", notified_socket)
                            continue

                        elif message == "[EXIT]":
                            print('Closed connection')
                            # Remove from our list of users
                            notified_socket.close()
                            self.active_connections.remove(notified_socket)

                            continue
                        elif message:
                            self.broadcast(message)
                            print(message)
                        else:
                            #closed connection violently, cleanup
                            notified_socket.close()
                            self.active_connections.remove(notified_socket)




                # It's not really necessary to have this, but will handle some socket exceptions just in case
                for notified_socket in exception_sockets:

                    # Remove from list
                    notified_socket.close()
                    self.active_connections.remove(notified_socket)
        except:
            print("server failed to start")
            self.close()

    def broadcast(self,message):
        # Iterate over connected clients and broadcast message
        for active_connection in self.active_connections:
            if active_connection != self.socket:
                self.send(message,active_connection)




def main(address):
    LOCALHOST, LOCALPORT=address
    server = SocketServer(LOCALHOST,LOCALPORT,SocketServer.LISTENMODE)
    server.start()

if __name__ == "__main__":
    lhost = "127.0.0.1"
    lport = 5050
    main((lhost, lport))
