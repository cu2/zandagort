"""
Zandagort server

Usage:
python server.py
"""

import errno
import json
import sys
import datetime
import Cookie
from urlparse import urlparse, parse_qs
import Queue
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from socket import error as socket_error

import config
from game import Game
from mycron import MyCron
from myenum import MyEnum


class InnerCommands(MyEnum):

    values = ["Sim", "Dump"]


class ZandagortRequestHandler(BaseHTTPRequestHandler):
    
    server_version = config.ZANDAGORT_SERVER_VERSION
    
    def do_GET(self):
        url = urlparse(self.path)
        command = url.path
        try:
            argument = json.dumps(self._parse_qs_flat(url.query))
        except Exception:
            argument = '{"error": "syntax_error"}'
        response = self._get_response("GET", command, argument)
        self._send_response(response)
    
    def do_POST(self):
        command = self.path
        try:
            request_body_length = int(self.headers.getheader("content-length"))
        except TypeError:
            request_body_length = 0
        try:
            argument = json.dumps(json.loads(self.rfile.read(request_body_length)))
        except Exception:
            argument = '{"error": "syntax_error"}'
        response = self._get_response("POST", command, argument)
        self._send_response(response)
    
    def log_message(self, format, *args):
        pass
    
    def _get_response(self, method, command, argument):
        my_queue = Queue.Queue()
        self.server._request_queue.put({
            "response_queue": my_queue,
            "method": method,
            "command": command,
            "argument": argument,
        })
        response = my_queue.get()
        my_queue.task_done()
        return response
    
    def _send_response(self, response, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type + "; charset=utf-8")
        self.send_header("Content-length", str(len(response)))
        auth_cookie_value = ""
        if "Cookie" in self.headers:
            cookies = Cookie.SimpleCookie(self.headers["Cookie"])
            for key in cookies:
                if key != config.AUTH_COOKIE_NAME:
                    self.send_header("Set-Cookie", cookies[key].output(header=""))
                else:
                    auth_cookie_value = cookies[key].value
        if auth_cookie_value.startswith("stuff"):  # TODO: replace test code with real
            try:
                x = int(auth_cookie_value[5:])
            except ValueError:
                x = 0
            auth_cookie_value = "stuff" + str(x+1)
        else:
            auth_cookie_value = "stuff"
        self._send_cookie(config.AUTH_COOKIE_NAME, auth_cookie_value, config.AUTH_COOKIE_EXPIRY, "/")
        self.end_headers()
        self.wfile.write(response)
    
    def _send_cookie(self, cookie_key, cookie_value, expires_from_now, path):
        C = Cookie.SimpleCookie()
        C[cookie_key] = cookie_value
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_from_now)
        C[cookie_key]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        C[cookie_key]["path"] = path
        self.send_header("Set-Cookie", C.output(header=""))
    
    def _parse_qs_flat(self, query):
        deep_query_dict = parse_qs(query)
        flat_query_dict = {}
        for key in deep_query_dict:
            flat_query_dict[key] = deep_query_dict[key][0]
        return flat_query_dict


class ZandagortHTTPServer(ThreadingMixIn, HTTPServer):
    
    def __init__(self, server_address, request_queue):
        HTTPServer.__init__(self, server_address, ZandagortRequestHandler)  # can't use standard super() because HTTPServer is old-style class
        self._request_queue = request_queue
        self.daemon_threads = True


class ZandagortServer(object):
    
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._request_queue = Queue.Queue()
        self._server = ZandagortHTTPServer((self._host, self._port), self._request_queue)
        self._server_thread = threading.Thread(target=self._server.serve_forever, name="Server Thread")
        self._server_thread.daemon = True
        self._cron = MyCron(config.CRON_BASE_DELAY)
        self._cron.add_task("sim", config.CRON_SIM_INTERVAL, self._cron_fun, InnerCommands.Sim)
        self._cron.add_task("dump", config.CRON_DUMP_INTERVAL, self._cron_fun, InnerCommands.Dump)
        self._game = Game(10000)
    
    def start(self):
        self._server_thread.start()
        self._cron.start()
        print "Listening at " + self._host + ":" + str(self._port) + "..."
    
    def serve_forever(self):
        try:
            while True:
                try:
                    request = self._request_queue.get(True, 4)
                except Queue.Empty:
                    continue
                if "inner_command" in request:
                    self._execute_inner_command(request["inner_command"])
                else:
                    response = self._execute_client_request(request["method"], request["command"], request["argument"])
                    request["response_queue"].put(response)
                    del request["response_queue"]  # might be unnecessary
                self._request_queue.task_done()
        except KeyboardInterrupt, SystemExit:
            print ""
            print "Shutting down..."
        finally:
            self._server.shutdown()
    
    def _execute_inner_command(self, command):
        if command == InnerCommands.Sim:
            self._game.sim()
            print "[" + str(command) + "] game time =", self._game.get_time()
        elif command == InnerCommands.Dump:
            print "[" + str(command) +  "] Dumping..."
            # TODO: add dump feature
            print "[" + str(command) +  "] Dumped."
        else:
            print "[" + str(command) + "] Unknown command"
    
    def _execute_client_request(self, method, command, argument):
        print "[" + method + "]", command
        print "<argument>"
        print argument
        print "</argument>"
        response = json.dumps({
            "world_state": str(self._game.get_time())
        })
        return response
    
    def _cron_fun(self, command):
        self._request_queue.put({
            "inner_command": command
        })


def main():
    print "Launching Zandagort Server..."
    try:
        server = ZandagortServer(config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT)
    except socket_error as serr:
        if serr.errno == errno.EACCES:
            print "[ERROR] port " + str(config.ZANDAGORT_SERVER_PORT) + " already used by some other service."
            print "Change it in config.py"
            return
        else:
            raise
    server.start()
    server.serve_forever()
    print "Zandagort Server shut down."


if __name__ == "__main__":
    main()
