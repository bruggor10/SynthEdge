from pythonosc import udp_client

class OSCSender:
    def __init__(self, ip, port):
        """
        Initialisiert den OSC Client.
        :param ip: IP-Adresse des OSC-Servers (Empfängers)
        :param port: Port des OSC-Servers
        """
        self.client = udp_client.SimpleUDPClient(ip, port)

    def send_message(self, address, *args):
        """
        Sendet eine OSC-Nachricht an die angegebene Adresse.
        :param address: OSC-Adresse (z. B. "/wek/inputs")
        :param args: Beliebig viele Werte, z. B. float, int, str
        """
        self.client.send_message(address, args)
        # print(f"Gesendet: {address} {args}")