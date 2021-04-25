from pydantic import HttpUrl
from feed_generator.generators import royalroad, aoa, ffnet

mapping = {
    'www.royalroad.com': royalroad,
    'royalroad.com': royalroad,
    'www.fanfiction.net': ffnet,
    'fanfiction.net': ffnet,
    'archiveofourown.org': aoa,
    'archiveofourown.org': aoa,
}

def from_url(url: HttpUrl):
    generator = mapping.get(url.host)
    if not generator:
        raise Exception()
    return generator
