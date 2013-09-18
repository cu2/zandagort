import httplib
import sys
import config


def client(ip, port, url, body):
    conn = httplib.HTTPConnection(ip, port)
    print "Sending...", body
    try:
#        conn.request("POST", url, body)
        conn.request("GET", url)
    except Exception:
        print "[ERROR] Zandagort Server not available at " + ip + ":" + str(port)
        conn.close()
        return
    try:
        resp = conn.getresponse()
    except Exception:
        print "[ERROR] Some problem occured..."
        conn.close()
        return
    print "status:", resp.status
    print "reason:", resp.reason
    print "<headers>"
    for header, value in resp.getheaders():
        print header, ":::", value
    print "</headers>"
    print "<body>"
    print resp.read()
    print "</body>"
    conn.close()


def main(args):
    if len(args) < 1:
        print "Usage: python zandagort_client.py <url>"
        return
    client(config.ZANDAGORT_SERVER_HOST, config.ZANDAGORT_SERVER_PORT, "someurl", args[0])


if __name__ == "__main__":
    main(sys.argv[1:])
