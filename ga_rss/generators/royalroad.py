from datetime import datetime
from datetime import timezone
import typing
from urllib.request import urlopen, Request
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0'

def generate_feed(feed_config: dict):
    rss_feed = FeedGenerator()
    rss_feed.id(feed_config['url'])
    rss_feed.title(feed_config['name'])

    req = Request(feed_config['url'], data=None, headers={'User-Agent': UA})
    with urlopen(req) as request:
        soup = BeautifulSoup(request.read(), features="html.parser")

    rss_feed.author({
        'name': soup.find('meta', {'property': 'books:author'})['content'],
        'email': 'test@example.com'
    })
    rss_feed.description(soup.find('meta', {'name': 'description'})['content'])
    rss_feed.link( href=feed_config['url'], rel='alternate' )
    rss_feed.logo(soup.find('div', class_='row fic-header').find('img')['src'])
    rss_feed.language('en')

    for chapter in soup.find(id='chapters').find_all('tr')[1:]:
        feed_entry = rss_feed.add_entry()
        link = urljoin(feed_config['url'], chapter.find('a')['href'])
        time = datetime.strptime(chapter.find('time')['title'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=timezone.utc)
        title = chapter.find('a').text.strip()

        feed_entry.id(link)
        feed_entry.title(title)
        feed_entry.description(title)
        feed_entry.link( href=link, rel='alternate' )
        feed_entry.published(time)

    return rss_feed


