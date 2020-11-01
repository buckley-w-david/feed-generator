from setuptools import find_packages, setup

setup(
    name='ga_rss',
    version='0.1.0',
    author='David Buckley',
    author_email='david@davidbuckley.ca',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'toml',
        'feedgen'
    ]
)