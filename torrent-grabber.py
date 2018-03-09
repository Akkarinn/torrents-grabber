from torrent_fetcher.http.Request import Request
from torrent_fetcher.sources.SourcesLoader import SourcesLoader

import json
import logging
import os
import sys

def initLogging():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

def getPatterns(pattern_filepath):
    try:
        return json.load(open(pattern_filepath))
    except:
        logging.error("An error occured while loading patterns file")
        raise

def main(argv):
    config_filepath = argv[1]
    patterns = getPatterns(argv[2])
    output_path = argv[3]

    sources = SourcesLoader.load(config_filepath)
    if not len(sources):
        logging.info("No sources: nothing to load")
        return False
    else:
        logging.info("Downloading torrents...")
        requester = Request(user_agent="torrent-grabber python")
        for s in sources:
            for torrent_uri in s.getTorrentsUrls(patterns):
                logging.info("+ %s" % (torrent_uri))
                requester.download(torrent_uri, output_path)
        logging.info("Downloading torrents completed")

    return True


if __name__ == "__main__":
    initLogging()
    if len(sys.argv) < 4:
        logging.error("Usage: %s <sources-loader-config-filepath> <torrents-pattern-filepath> <output-directory>", sys.argv[0])
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        logging.error("Configuration file %r was not found!", sys.argv[1])
        sys.exit(1)
    if not os.path.exists(sys.argv[2]):
        logging.error("Pattern file %r was not found!", sys.argv[1])
        sys.exit(1)
    if not os.path.exists(sys.argv[3]):
        logging.error("Directory %r was not found!", sys.argv[2])
        sys.exit(1)

    try:
        if main(sys.argv):
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        sys.stderr.write("Exception: %s"%(str(e)))
        sys.exit(1)