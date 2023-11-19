import socket
import re

class Sr201:
    _IPV4_RE = '[.]'.join(('(?:[0-9]{1,2}|[01][0-9]{2}|2[0-4][0-9]|25[0-5])',) * 4)
    PORT_CONFIG = 5111
    PORT_CONTROL = 6722

    def __init__(self, hostname):
        self._hostname = hostname
        self._port = None
        self._soc = None

    def open(self, port=None):
        port = port or self.PORT_CONTROL
        if port == self._port:
            self.flush()
            return
        self.close()
        self._soc = socket.create_connection((self._hostname, port))
        self._port = port

    def close(self):
        if self._soc:
            self.flush()
            self._soc.close()
            self._port = None
            self._soc = None

    def flush(self):
        while True:
            try:
                data = self._soc.recv(4096)
                if not data:
                    break
            except socket.error:
                break

    def send(self, data):
        return self._soc.send(data.encode('latin1'))

    def recv(self):
        response = self._soc.recv(4096).decode('latin1')
        return response

    def send_config(self, command, op, value):
        self.open(self.PORT_CONFIG)
        param = value is not None and ',' + value or ''
        self.send('#' + op + '9999' + param + ';')
        response = self.recv()
        if (
            not response or response[0] != '>' or response[-1] != ';' or
            op != '1' and response != '>OK;'
        ):
            raise Exception(f"Invalid response to {command}: {response}")
        return response

    def do_ip(self, command):
        match = re.match('ip=(' + self._IPV4_RE + ')$', command)
        if not match:
            raise ValueError(f"Invalid {command}")
        self.send_config(command, '2', match.group(1))

    def save_and_restart(self):
        self.send_config('save_and_restart', '7', '')

def change_ip_address(hostname, new_ip):
    device = Sr201(hostname)
    device.open()
    device.do_ip(f"ip={new_ip}")
    device.save_and_restart()
    device.close()


# Example usage: CURRENT ADDRESS to NEW ADDRESS
change_ip_address("192.168.1.100", "192.168.1.98")
