import fanficfare
from fanficfare import adapters, writers, exceptions
from fanficfare.configurable import Configuration

def fetch_metadata(url: str, chapters = True) -> bytes:
    configuration = Configuration(adapters.getConfigSectionsFor(url), 'epub')
    adapter = adapters.getAdapter(configuration, url)
    adapter.is_adult = True
    metadata = adapter.getStoryMetadataOnly().getAllMetadata()

    if chapters:
        metadata['zchapters'] = []
        for i, chap in enumerate(adapter.get_chapters()):
            metadata['zchapters'].append((i+1, chap))

    return metadata

