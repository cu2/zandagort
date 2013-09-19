import Queue
import sys
import threading
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import config


class ZandagortRequestHandler(BaseHTTPRequestHandler):
    
    server_version = "Zandagort/2.0"
    
    def do_GET(self):
        cur_thread = threading.current_thread()
        msg = self.path
        my_queue = Queue.Queue()
        self.server.request_queue.put((my_queue, "Check this out: " + msg))
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


def cron(request_queue):
    while True:
        time.sleep(1)
        my_queue = Queue.Queue()
        request_queue.put((my_queue, "[CRON]"))
        response = my_queue.get()
        my_queue.task_done()


def main():
    world_state = 0
    request_queue = Queue.Queue()
    print "[Main Thread] Launching Zandagort Server..."
    server = ZandagortServer((config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT), ZandagortRequestHandler, request_queue)
    server_thread = threading.Thread(target=server.serve_forever, name="Server Thread")
    server_thread.daemon = True
    server_thread.start()
    print "[Main Thread] Server Thread listening."
    cron_thread = threading.Thread(target=cron, name="Cron Thread", args=(request_queue,))
    cron_thread.daemon = True
    cron_thread.start()
    try:
        while True:
            try:
                response_queue, msg = request_queue.get(True, 4)
            except Queue.Empty:
                continue
            print "[Main Thread] Got msg: " + msg
            if msg == "[CRON]":
                world_state += 1
            print "[Main Thread] world_state =", world_state
            response_queue.put("world_state = " + str(world_state))
            del response_queue  # might be unnecessary
            request_queue.task_done()
    except KeyboardInterrupt, SystemExit:
        print "[Main Thread] Shutting down Zandagort Server..."
    finally:
        server.shutdown()
    print "[Main Thread] Zandagort Server shut down."


if __name__ == "__main__":
    main()
