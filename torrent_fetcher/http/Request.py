import logging
import os
import urllib3

class Request():
    def __init__(self, user_agent):
        self.user_agent_ = user_agent

    # Request a given uri according to the given method (GET)
    def get(self, resource_uri, decode=True):
        try:
            http = urllib3.PoolManager()
            req = http.request('GET', resource_uri, { 'User-Agent' : self.user_agent_ })
        except:
            logging.error("[Http][Request] Unable to GET '%s'" % (resource_uri))
            raise
        if decode:
            return req.data.decode('utf-8')
        return req.data

    def download(self, resource_uri, destination_path):
        data = self.get(resource_uri, decode=False)
        destination_path = str("%s/%s" % (destination_path, os.path.split(resource_uri)[-1]))
        try:
            out = open(destination_path, "wb")
            out.write(data)
        except:
            logging.error("[Http][Request] Unable to write to '%s'" % (destination_path))
            raise

