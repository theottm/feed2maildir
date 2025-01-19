import feedparser
from multiprocessing.pool import ThreadPool

def fetch_and_parse_feed(args):
    name, feed = args
    return (name, feedparser.parse(feed))

class Reader:
    """Get updates on the feeds supplied"""

    def __init__(self, feeds, silent=False, njobs=4):
        self.feeds = []
        self.silent = silent
        with ThreadPool(processes=njobs) as pool:
            for feed, f in map(fetch_and_parse_feed, feeds.items()):
                print(f"Parsing: {feed}")
                if f.bozo:
                    self.output('WARNING: Could not fully parse feed: {}'.format(feed))
                f.feed_alias_name = feed # user provided text
                self.feeds.append(f)

    def output(self, arg):
        if not self.silent:
            print(arg)

