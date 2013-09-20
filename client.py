"""
Simple commandline client for Zandagort

Usage:
python client.py <host> <port>

Commands:
1. GET/POST
2. command
3. arguments

Argument format:
- GET: key=value(&key=value)*
- POST: json
"""

import httplib
import sys


class ZandagortClient(object):
    
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._conn = httplib.HTTPConnection(host, port)
    
    def connect(self):
        try:
            self._conn.connect()
        except Exception:
            print "[ERROR] Zandagort Server not available at " + self._host + ":" + str(self._port)
            return False
        return True
    
    def send_get(self, command, arguments=""):
        url = command
        if arguments:
            url += "?" + arguments
        return self._send_request("GET", url)
    
    def send_post(self, command, arguments=""):
        return self._send_request("POST", command, arguments)
    
    def _send_request(self, method, url, body=""):
        try:
            self._conn.request(method, url, body)
        except Exception:
            print "[ERROR] Zandagort Server not available at " + self._host + ":" + str(self._port)
            return False
        try:
            resp = self._conn.getresponse()
        except Exception:
            print "[ERROR] Some problem occured..."
            return False
        if resp.status == 200:
            print "<response>"
            print resp.read()
            print "</response>"
        else:
            print "[ERROR]", resp.status
        return True
    
    def reset(self):
        self._conn.close()
        return self.connect()
    
    def shutdown(self):
        self._conn.close()


def main(args):
    if len(args) < 2:
        print "Usage: python client.py <host> <port>"
        return
    client = ZandagortClient(args[0], int(args[1]))
    if not client.connect():
        return
    print "Client running. Press <Ctrl+C> to stop."
    try:
        while True:
            method = raw_input("GET/POST? ")
            is_get = method[0].upper() == "G"
            command = raw_input("Command: ")
            arguments = raw_input("Arguments: ")
            if is_get:
                success = client.send_get(command, arguments)
            else:
                success = client.send_post(command, arguments)
            if not success:
                if not client.reset():
                    return
    except KeyboardInterrupt, SystemExit:
        client.shutdown()
        print ""
        print "Client shut down."


if __name__ == "__main__":
    main(sys.argv[1:])
