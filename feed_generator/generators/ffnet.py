from datetime import datetime
from datetime import timezone
import typing
from urllib.request import urlopen, Request
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

from feed_generator.config import FeedModel

UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'

def generate_feed(feed_config: FeedModel):
    rss_feed = FeedGenerator()
    rss_feed.id(feed_config.url)
    rss_feed.title(feed_config.name)

    req = Request(feed_config.url, data=None, headers={'User-Agent': UA})
    with urlopen(req) as request:
        soup = BeautifulSoup(request.read(), features="lxml")

    rss_feed.author({
        'name':  soup.find(id='profile_top').find('a').text,
        'email': 'test@example.com'
    })
    rss_feed.description(soup.find(id='profile_top').find('div', {"class": "xcontrast_txt"}).text)
    rss_feed.link( href=feed_config.url, rel='alternate' )
    rss_feed.language('en')

    for chapter in soup.find(id='chap_select').find_all('option'):
        feed_entry = rss_feed.add_entry()
        link = urljoin(feed_config.url, chapter['value'])
        time = datetime.utcnow().replace(tzinfo=timezone.utc) #FIXME
        title = chapter.text

        feed_entry.id(link)
        feed_entry.title(title)
        feed_entry.description(title)
        feed_entry.link( href=link, rel='alternate' )
        feed_entry.published(time)

    return rss_feed


