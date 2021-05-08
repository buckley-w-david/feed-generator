import fanficfare
from fanficfare import adapters, writers, exceptions
from fanficfare.configurable import Configuration

def fetch_metadata(url: str) -> bytes:
    configuration = Configuration(adapters.getConfigSectionsFor(url), 'epub')
    adapter = adapters.getAdapter(configuration, url)
    adapter.is_adult = True
    metadata = adapter.getStoryMetadataOnly().getAllMetadata()

    return metadata

