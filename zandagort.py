"""
Zandagort server

Usage:
python server.py
"""

import json
import sys
import time
from urlparse import urlparse, parse_qs
import Queue
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

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
            deep_query_dict = parse_qs(url.query, False, True)
            argument = json.dumps(self._flatten_query_dict(deep_query_dict))
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
    
    def _send_response(self, response):
        response_length = len(response)
        self.send_response(200)
        self.send_header("Content-length", str(response_length))
        self.wfile.write("\n" + response)
    
    def _flatten_query_dict(self, deep_query_dict):
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
        response = "world_state = " + str(self._game.get_time())
        return response
    
    def _cron_fun(self, command):
        self._request_queue.put({
            "inner_command": command
        })


def main():
    print "Launching Zandagort Server..."
    server = ZandagortServer(config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT)
    server.start()
    server.serve_forever()
    print "Zandagort Server shut down."


if __name__ == "__main__":
    main()
