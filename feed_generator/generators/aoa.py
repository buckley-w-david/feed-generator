from datetime import datetime
from datetime import timezone
import typing
from urllib.request import urlopen, Request
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from feedgen.feed import FeedGenerator

from feed_generator.config import FeedModel

UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

def generate_feed(feed_config: FeedModel):
    rss_feed = FeedGenerator()
    rss_feed.id(feed_config.url)
    rss_feed.title(feed_config.name)

    req = Request(f"{feed_config.url}/navigate", data=None, headers={'User-Agent': UA})
    with urlopen(req) as request:
        soup = BeautifulSoup(request.read(), features="html.parser")

    rss_feed.author({
        'name': soup.find('a', {'rel': 'author'}).text,
        'email': 'test@example.com'
    })
    rss_feed.description(soup.find('h2', {'class': 'heading'}).find('a').text)
    rss_feed.link( href=feed_config.url, rel='alternate' )
    rss_feed.language('en')

    for chapter in soup.find(id='main').find_all('li'):
        feed_entry = rss_feed.add_entry()
        link = urljoin(feed_config.url, chapter.find('a')['href'])
        time = datetime.strptime(chapter.find(class_='datetime').text, '(%Y-%m-%d)').replace(tzinfo=timezone.utc)
        title = chapter.find('a').text.strip()

        feed_entry.id(link)
        feed_entry.title(title)
        feed_entry.description(title)
        feed_entry.link( href=link, rel='alternate' )
        feed_entry.published(time)

    return rss_feed


