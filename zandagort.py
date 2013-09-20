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
    
    def _get_response(self, method, command, argument):
        my_queue = Queue.Queue()
        self.server.request_queue.put({
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
    
    def log_message(self, format, *args):
        pass
    
    def _flatten_query_dict(self, deep_query_dict):
        flat_query_dict = {}
        for key in deep_query_dict:
            flat_query_dict[key] = deep_query_dict[key][0]
        return flat_query_dict


class ZandagortHTTPServer(ThreadingMixIn, HTTPServer):
    
    def __init__(self, server_address, RequestHandlerClass, request_queue):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)  # can't use standard super() because HTTPServer is old-style class
        self.request_queue = request_queue
        self.daemon_threads = True


def cron_fun(request_queue, cmd):
    request_queue.put({
        "cmd": cmd
    })


def main():
    print "Launching Zandagort Server..."
    game = Game(10000)
    world_state = 0
    request_queue = Queue.Queue()
    server = ZandagortHTTPServer((config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT), ZandagortRequestHandler, request_queue)
    server_thread = threading.Thread(target=server.serve_forever, name="Server Thread")
    server_thread.daemon = True
    server_thread.start()
    print "Listening at " + config.ZANDAGORT_SERVER_HOST + ":" + str(config.ZANDAGORT_SERVER_PORT) + "..."
    cron = MyCron(config.CRON_BASE_DELAY)
    cron.add_task("sim", config.CRON_SIM_INTERVAL, cron_fun, request_queue, "[SIM]")
    cron.add_task("dump", config.CRON_DUMP_INTERVAL, cron_fun, request_queue, "[DUMP]")
    cron.start()
    try:
        while True:
            try:
                request = request_queue.get(True, 4)
            except Queue.Empty:
                continue
            if "cmd" in request:
                if request["cmd"] == "[SIM]":
                    world_state += 1
                    game.sim()
                    print "[SIM] world_state =", world_state
                elif request["cmd"] == "[DUMP]":
                    print "[DUMP] Dump!!!"
                else:
                    print "[???] Unknown command: ", request["cmd"]
            else:
                print "[" + request["method"] + "]", request["command"]
                print "<argument>"
                print request["argument"]
                print "</argument>"
                request["response_queue"].put("world_state = " + str(world_state))
                del request["response_queue"]  # might be unnecessary
                request_queue.task_done()
    except KeyboardInterrupt, SystemExit:
        print ""
        print "Shutting down..."
    finally:
        server.shutdown()
    print "Zandagort Server shut down."


if __name__ == "__main__":
    main()
