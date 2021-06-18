from datetime import datetime
from datetime import timezone
import typing
from urllib.request import urlopen, Request
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

from feed_generator.config import FeedModel
from feed_generator.metadata import fetch_metadata

def generate_feed(feed_config: FeedModel):
    rss_feed = FeedGenerator()
    rss_feed.id(feed_config.url)
    rss_feed.title(feed_config.name)

    metadata = fetch_metadata(feed_config.url)

    rss_feed.author({
        'name': metadata['author'],
        'email': f"{metadata['author']}@{feed_config.url.host}"
    })
    rss_feed.description(metadata['description'])
    rss_feed.link( href=feed_config.url, rel='alternate' )
    rss_feed.logo(metadata['cover_image'])
    rss_feed.language('en')

    for i, chapter in metadata['zchapters']:
        feed_entry = rss_feed.add_entry()
        link = chapter['url']
        time = datetime.strptime(metadata['dateUpdated'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        title = chapter['title']

        feed_entry.id(link)
        feed_entry.title(title)
        feed_entry.description(title)
        feed_entry.link( href=link, rel='alternate' )
        feed_entry.published(time)

    return rss_feed


