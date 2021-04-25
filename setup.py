from setuptools import find_packages, setup

setup(
    name='feed_generator',
    version='0.1.0',
    author='David Buckley',
    author_email='david@davidbuckley.ca',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'toml',
        'feedgen',
        'lxml',
        'typer',
    ],
    entry_points = {
        'console_scripts': [
            'feed-generator=feed_generator.feed:app'
        ]
    }
)
