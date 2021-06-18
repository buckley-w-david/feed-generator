from pydantic import HttpUrl

from fanficfare import exceptions, adapters
from fanficfare.configurable import Configuration

from feed_generator.generators import royalroad, aoa
from feed_generator.generators import fanficfare as fanficfare_generator

mapping = {
    'www.royalroad.com': royalroad,
    'royalroad.com': royalroad,
    'archiveofourown.org': aoa,
}

def from_url(url: HttpUrl):
    fff_works = False
    try:
        configuration = Configuration(adapters.getConfigSectionsFor(str(url)), 'epub')
        fff_works = True
    except exceptions.UnknownSite:
        pass

    generator = mapping.get(url.host)
    if generator:
        return generator
    elif fff_works:
        return fanficfare_generator
    raise Exception()
