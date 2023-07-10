import socket
import netifaces as ni


class Connection:
    # Common default connection values
    PORT_REGEX = "^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
    IP_REGEX = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    ENCODETYPE = 'utf-8'
    HEADERSIZE = 1024
    PROTOCOL = socket.AF_INET
    CONNECTIONTYPE = socket.SOCK_STREAM
    # set up socket

    def __init__(self, ip, port, encode_type=ENCODETYPE, header_size=HEADERSIZE, protocol=PROTOCOL, connection_type=CONNECTIONTYPE):
        self.ip = ip
        self.port = port
        self.header_size = header_size
        self.clients = []
        self.encode_type = encode_type
        self.socket = socket.socket(protocol, connection_type)

    # gets the ip address of the interface passed in
    @staticmethod
    def get_ip_address(interface):
        return ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

    '''
    move to switch class
    @staticmethod
    def check_ip_address(ip):
        # pass the regular expression
        # and the string in search() method
        return True if re.search(Connection.IP_REGEX,ip) else False

    @staticmethod
    def check_port_number(port):
        return True if re.search(Connection.PORT_REGEX,port) else False
    '''
    # close socket

    def close(self):
        self.socket.close()

    def send(self, message, _socket):

        try:
            # Create header containing the length of the next message padded with the size of the heading
            # encode data
            # header not defined
            # header = f"{len(message):<{self.header_size}}"
            header = ""
            body = message
            data = header + body
            encoded_data = data.encode(self.encode_type)
            # send data to remote host
            _socket.send(encoded_data)
        except Exception as e:
            print("Failed to send message\n{e}")

    # Handles message receiving

    def receive(self, _socket):
        try:

            # Receive our "header" containing message length, it's size is defined and constant
            message_header = _socket.recv(self.header_size)

            # If we received no data, connection closed softly, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not message_header:
                return False

            # Convert header to int value
            message_length = len(message_header.decode('utf-8').strip())

            # Return an object of message header and message data
            return message_header

        except Exception as e:

            # If we are here,then the connection closed violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            print(f"Something is wrong with the message header.\n{e}")
