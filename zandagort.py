"""
Zandagort server

Usage:
python server.py

GET command:
<command>?<arguments>
<arguments>= <key>=<value>[&<key>=<value>]*

POST command:
<command> in header, <arguments> in body
<arguments>= JSON

Response:
JSON

"""

import errno
import json
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
from getcontroller import GetController
from postcontroller import PostController


class InnerCommands(MyEnum):  # pylint: disable-msg=R0903
    """Inner commands for ZandagortServer"""

    values = ["Sim", "Dump"]


def _parse_qs_flat(query):
    """Return flat version of parse_qs. 'q=a,b' becomes "q":"a,b" not "q":["a","b"]"""
    deep_query_dict = parse_qs(query)
    flat_query_dict = {}
    for key in deep_query_dict:
        flat_query_dict[key] = deep_query_dict[key][0]
    return flat_query_dict


class ZandagortRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for ZandagortHTTPServer"""
    
    server_version = config.SERVER_VERSION
    
    def do_GET(self):
        """Handle GET requests"""
        url = urlparse(self.path)
        command = url.path.lstrip("/")
        if command == "test" or command == "test/":
            self._send_static_file("html/test.html")
            return
        if command.startswith("static/"):
            self._send_static_file(command[7:])
            return
        if command == "favicon.ico":
            self._send_static_file("img/favicon.ico", "image/x-icon")
            return
        try:
            arguments = _parse_qs_flat(url.query)
        except Exception:
            arguments = {"error": "Syntax error"}
        response = self._get_response("GET", command, arguments)
        self._send_response(json.dumps(response))
    
    def do_POST(self):
        """Handle POST requests"""
        command = self.path.lstrip("/")
        try:
            request_body_length = int(self.headers.getheader("content-length"))
        except TypeError:
            request_body_length = 0
        try:
            arguments = json.loads(self.rfile.read(request_body_length))
        except Exception:
            arguments = {"error": "Syntax error"}
        response = self._get_response("POST", command, arguments)
        self._send_response(json.dumps(response))
    
    def log_message(self, format_, *args):
        """Overwrite (disable) default logging"""
        pass
    
    def _get_response(self, method, command, arguments):
        """Get response from core Zandagort Server"""
        my_queue = Queue.Queue()
        self.server.request_queue.put({
            "response_queue": my_queue,
            "method": method,
            "command": command,
            "arguments": arguments,
        })
        response = my_queue.get()
        my_queue.task_done()
        return response
    
    def _send_response(self, response, content_type="application/json"):
        """Send response to client"""
        self.send_response(200)
        self.send_header("Content-type", content_type + "; charset=utf-8")
        self.send_header("Content-length", str(len(response)))
        auth_cookie_value = ""
        if "Cookie" in self.headers:
            cookies = Cookie.SimpleCookie(self.headers["Cookie"])
            if config.AUTH_COOKIE_NAME in cookies:
                auth_cookie_value = cookies[config.AUTH_COOKIE_NAME].value
        if auth_cookie_value.startswith("stuff"):  # TODO: replace test code with real
            try:
                counter = int(auth_cookie_value[5:])
            except ValueError:
                counter = 0
            auth_cookie_value = "stuff" + str(counter+1)
        else:
            auth_cookie_value = "stuff"
        self._send_cookie(config.AUTH_COOKIE_NAME, auth_cookie_value, config.AUTH_COOKIE_EXPIRY, "/")
        self.end_headers()
        self.wfile.write(response)
    
    def _send_cookie(self, cookie_key, cookie_value, expires_from_now, path):
        """Send cookie with key, value, expiry and path"""
        cookie = Cookie.SimpleCookie()
        cookie[cookie_key] = cookie_value
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_from_now)
        cookie[cookie_key]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        cookie[cookie_key]["path"] = path
        self.send_header("Set-Cookie", cookie.output(header=""))
    
    def _send_static_file(self, filename, content_type=None):
        """Send static file to client"""
        content = ""
        if content_type is None:
            try:
                file_type = filename[:filename.index("/")]
            except ValueError:
                file_type = "?"
            if file_type == "js":
                content_type = "text/javascript"
            elif file_type == "css":
                content_type = "text/css"
            else:
                content_type = "text/html"
        with open("static/" + filename, "r") as infile:
            content = infile.read()
        self._send_response(content, content_type)


class ZandagortHTTPServer(ThreadingMixIn, HTTPServer):
    """Multi threaded HTTP server between clients and ZandagortServer"""
    
    def __init__(self, server_address, request_queue):
        HTTPServer.__init__(self, server_address, ZandagortRequestHandler)  # can't use standard super() because HTTPServer is old-style class
        self.request_queue = request_queue
        self.daemon_threads = True


class ZandagortServer(object):
    """Single threaded core server to handle Game"""
    
    def __init__(self, host, port):
        self._address = (host, port)
        self._request_queue = Queue.Queue()
        self._server = ZandagortHTTPServer(self._address, self._request_queue)
        self._server_thread = threading.Thread(target=self._server.serve_forever, name="Server Thread")
        self._server_thread.daemon = True
        self._cron = MyCron(config.CRON_BASE_DELAY)
        self._cron.add_task("sim", config.CRON_SIM_INTERVAL, self._cron_fun, InnerCommands.Sim)
        self._cron.add_task("dump", config.CRON_DUMP_INTERVAL, self._cron_fun, InnerCommands.Dump)
        self._game = Game(10000)
        self._controllers = {
            "GET": GetController(self._game._world),
            "POST": PostController(self._game._world),
        }
        self._logfiles = {}
        for key in config.SERVER_LOG_FILES:
            self._logfiles[key] = open(config.SERVER_LOG_DIR + "/" + config.SERVER_LOG_FILES[key], "a", 1)  # line buffered
    
    def start(self):
        """Start server and cron threads"""
        self._server_thread.start()
        self._cron.start()
        self._log_sys("Listening at " + self._address[0] + ":" + str(self._address[1]) + "...")
    
    def serve_forever(self):
        """Main loop of core server"""
        try:
            while True:
                try:
                    request = self._request_queue.get(True, 4)
                except Queue.Empty:
                    continue
                if "inner_command" in request:
                    self._execute_inner_command(request["inner_command"])
                else:
                    response = self._execute_client_request(request["method"], request["command"], request["arguments"])
                    request["response_queue"].put(response)
                    del request["response_queue"]  # might be unnecessary
                self._request_queue.task_done()
        except (KeyboardInterrupt, SystemExit):
            self._log_sys("Shutting down...")
        finally:
            self._server.shutdown()  # shutdown http server
            self._shutdown()  # shutdown zandagort server
    
    def _shutdown(self):
        """Close logfiles"""
        for key in self._logfiles:
            self._logfiles[key].close()
    
    def _execute_inner_command(self, command):
        """Execute inner commands like Sim or Dump"""
        if command == InnerCommands.Sim:
            self._game.sim()
            self._log_sys("[" + str(command) + "] game time = " + str(self._game.get_time()))
        elif command == InnerCommands.Dump:
            self._log_sys("[" + str(command) +  "] Dumping...")
            # TODO: add dump feature
            self._log_sys("[" + str(command) +  "] Dumped.")
        else:
            self._log_sys("[" + str(command) + "] Unknown command")
    
    def _execute_client_request(self, method, command, arguments):
        """Execute commands sent by clients"""
        if method == "GET":
            try:
                query_string = "&".join([key+"="+arguments[key] for key in arguments])
            except Exception:
                query_string = "[ERROR]"
            request_string = "[" + method + "] " + command + "?" + query_string
        else:
            request_string = "[" + method + "] " + command
        if method not in ["GET", "POST"]:
            self._log_error(request_string + " ! Unknown method")
            return {"error": "Unknown method"}
        try:
            controller_function = getattr(self._controllers[method], command)
        except AttributeError:
            self._log_error(request_string + " ! Unknown command")
            return {"error": "Unknown command"}
        try:
            response = controller_function(**arguments)
        except Exception:
            self._log_error(request_string + " ! Argument error")
            return {"error": "Argument error"}
        self._log_access(request_string)
        return response
    
    def _cron_fun(self, command):
        """Simple helper function for cron thread"""
        self._request_queue.put({
            "inner_command": command
        })
    
    def _log(self, logtype, message):
        """General log function for file and stdout"""
        message = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message
        if config.SERVER_LOG_STDOUT.get(logtype, "False"):
            print "[" + logtype.upper() + "] " + message
        if logtype in self._logfiles:
            self._logfiles[logtype].write(message + "\n")
    
    def _log_access(self, message):
        """Wrapper for access log"""
        self._log("access", message)
    
    def _log_error(self, message):
        """Wrapper for error log"""
        self._log("error", message)
    
    def _log_sys(self, message):
        """Wrapper for sys log"""
        self._log("sys", message)


def main():
    """Create, start and run Zandagort Server"""
    
    print "Launching Zandagort Server..."
    try:
        server = ZandagortServer(config.SERVER_HOST, config.SERVER_PORT)
    except socket_error as serr:
        if serr.errno == errno.EACCES:
            print "[ERROR] port " + str(config.SERVER_PORT) + " already used by some other service."
            print "Change it in config.py"
            return
        else:
            raise
    server.start()
    server.serve_forever()  # blocking call
    print "Zandagort Server shut down."


if __name__ == "__main__":
    main()
