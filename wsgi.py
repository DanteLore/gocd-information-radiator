import json
import os
from go.go_crazy import GoCrazy

url = os.environ['GOCD_SERVER']
username = os.environ['GOCD_USER']
password = os.environ['GOCD_PASSWORD']
disable_ssl = os.getenv('GOCD_DISABLE_SSL_CHECK', False)


def application(env, start_response):
    go = GoCrazy(url, username, password, disable_ssl)

    # TODO: put a cache in here to prevent access to GoCD if there are multiple clients connected

    # TODO: don't just handle every URL, be more specific!!

    result = go.get_build_status()
    start_response('200 OK', [('Content-Type', 'text/json')])
    return json.dumps(result)


if __name__ == "__main__":
    go = GoCrazy(url, username, password)
    result = go.get_build_status()
    print json.dumps(result)
