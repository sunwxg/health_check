from distutils.core import setup

config = {
    'description': 'health check log analysis',
    'author': 'sun wang',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': [],
    'packages': ['healthcheck'],
    'scripts': ['py.hc'],
    'name': 'health_check'
}

setup(**config)
