from twisted.internet import reactor
from quarry.net.client import ClientFactory, ClientProtocol



def get_status(ip):
    class PingProtocol(ClientProtocol):
        def status_response(self, data):
            print("inside")
            print(data)
            for k, v in sorted(data.items()):
                if k != "favicon":
                    self.logger.info("%s --> %s" % (k, v))

            reactor.stop()


    class PingFactory(ClientFactory):
        protocol: PingProtocol
        protocol_mode_next: str = 'status'


    factory = PingFactory()
    print(ip)
    factory.connect("play.pokesaga.org", 25565)
    reactor.run()


get_status("play.pokesaga.org")



