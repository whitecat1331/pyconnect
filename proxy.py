from server import SocketServer
from tinyhtml import html, h


class Proxy:

    ALL_INTERFACES = '0.0.0.0'

    def __init__(self, port, ip=ALL_INTERFACES):
        self.socket = SocketServer(ip, port)

    def listen(self):
        self.socket.start(self.build_response())


class HTTPProxy(Proxy):

    PORT = 80

    def __init__(self):
        Proxy.__init__(self, HTTPProxy.PORT)

    def build_response(self):
        # Constructing HTML using html() and h()
        # nested h() is also supported
        html_content = html(lang="en")(
            h("head")(
                (h("h1")("Malinfo Server")),
            ),
        ).render()

# printing html formed on console.
        return html_content


def main():
    http = HTTPProxy()
    http.listen()


if __name__ == "__main__":
    main()
