import Queue
import sys
import threading
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

import config
from mycron import MyCron


class ZandagortRequestHandler(BaseHTTPRequestHandler):
    
    server_version = "Zandagort/2.0"
    
    def do_GET(self):
        cur_thread = threading.current_thread()
        msg = self.path
        my_queue = Queue.Queue()
        self.server.request_queue.put({
            "response_queue": my_queue,
            "message": "Check this out: " + msg,
        })
        response = my_queue.get()
        print "[" + cur_thread.name + "] Got this: " + response
        my_queue.task_done()
        self.send_response(200, "You said " + self.path + ". Server response: " + response)
    
    def log_message(self, format, *args):
        cur_thread = threading.current_thread()
        print >>sys.stderr, "[" + cur_thread.name + "]", (format % args)


class ZandagortServer(ThreadingMixIn, HTTPServer):
    
    def __init__(self, server_address, RequestHandlerClass, request_queue):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)  # can't use standard super() because HTTPServer is old-style
        self.request_queue = request_queue
        self.daemon_threads = True


def cron_fun(request_queue, cmd):
    request_queue.put({
        "cmd": cmd
    })


def main():
    world_state = 0
    request_queue = Queue.Queue()
    print "[Main Thread] Launching Zandagort Server..."
    server = ZandagortServer((config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT), ZandagortRequestHandler, request_queue)
    server_thread = threading.Thread(target=server.serve_forever, name="Server Thread")
    server_thread.daemon = True
    server_thread.start()
    print "[Main Thread] Server Thread listening."
    cron = MyCron(1)
    cron.add_task("sim", 2, cron_fun, request_queue, "[SIM]")
    cron.add_task("dump", 5, cron_fun, request_queue, "[DUMP]")
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
                elif request["cmd"] == "[DUMP]":
                    print "[Main Thread] Dump!!!"
                else:
                    print "[Main Thread] Unknown command: ", request["cmd"]
            else:
                print "[Main Thread] From client: " + request["message"]
                request["response_queue"].put("world_state = " + str(world_state))
                del request["response_queue"]  # might be unnecessary
                request_queue.task_done()
            print "[Main Thread] world_state =", world_state
    except KeyboardInterrupt, SystemExit:
        print "[Main Thread] Shutting down Zandagort Server..."
    finally:
        server.shutdown()
    print "[Main Thread] Zandagort Server shut down."


if __name__ == "__main__":
    main()
