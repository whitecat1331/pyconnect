from connection.connection import Connection
import sys
class Client(Connection):
    def __init__(self,ip,port):
        super().__init__(ip,port)

    def connect(self):
        # Connect to a given ip and port
        self.socket.connect((self.ip, self.port))

        print(self.receive(self.socket))
        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        #self.socket.setblocking(False)



    def start(self):
        while True:
            try:
                message = input("Enter message to send: ")
                # If message is not empty - send it
                if not message:
                    self.send("[REFRESH]",self.socket)
                    response = self.receive(self.socket)
                elif message == "exit":
                    self.send("[EXIT]", self.socket)
                    self.close()
                    sys.exit()
                else:
                    print(f"sending {message}")
                    self.send(message,self.socket)
                    print("Waiting to receive data")
                    response = self.receive(self.socket)
                # Print message
                print(f'{response}')

            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))

                    # We just did not receive anything
                continue

            except Exception as e:
                # Any other exception - something happened, exit
                print('Error: '.format(str(e)))




def main():
    REMOTEHOST = "127.0.0.1"
    REMOTEPORT = 5050

    client = Client(REMOTEHOST,REMOTEPORT)
    client.connect()
    client.start()

if __name__ == "__main__":
    main()
