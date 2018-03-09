from torrent_fetcher.sources.AbstractSource import AbstractSource
from torrent_fetcher.http.Request import Request
from bs4 import BeautifulSoup
import logging
import os
import re

def initLogging():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

class Source(AbstractSource):

    def __init__(self):
        super().__init__()
        self.requester_ = Request(user_agent="torrent-grabber python")

    def getTorrentsUrls(self, requestedPatterns):
        """
        Get torrent urls from the source according to the given requestPatterns

        :param requestedPatterns: regex expression to look for in the source.
        :return: a collection of torrent urls
        """
        logging.info("[Source][torrent9] Fetch torrents urls")
        main_page = self.requester_.get("http://www.torrent9.red/view_cat.php?categorie=series&trie=date-d")
        links = self.__extractItemsLinks(main_page)
        selected_links = self.__matchItemLinks(links, requestedPatterns)
        logging.info("[Source][torrent9] Found %s torrents matching the input patterns" % (len(selected_links)))
        return self.__extractTorrentFromLinks(selected_links)

    def __extractItemsLinks(self, content):
        soup = BeautifulSoup(content, "html.parser")
        return [str(link.get("href")) for link in soup.find_all('a')]

    def __matchItemLinks(self, links, requestedPatterns):
        selected_link = []
        for p in requestedPatterns:
            selected_link += list(
                map(lambda m: m.group(),
                        filter(lambda m: m is not None,
                               [re.match(p, link) for link in links])))
        return selected_link

    def __extractTorrentFromLinks(self, links):
        basename = "http://www.torrent9.red/get_torrent/"
        return [basename + os.path.basename(lnk) + ".torrent" for lnk in links]

def createSource():
    return Source()

if __name__ == "__main__":
    initLogging()
    source = createSource()
    patterns = [".*dragon-ball-super.*vostfr-hdtv.*", ".*alienist.*vostfr.*"]
    print(source.getTorrentsUrls(patterns))
