import sys

from meta import _META as META
from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit('Python < 3 is unsupported.')

url_template = 'https://github.com/maxvanceffer/fs-syncer/archive/v%s.tar.gz'
requirements = []

setup(
    name='fs-syncer',
    version= META['version'],
    packages=['syncer', 'qml', 'bin'],
    license='MIT',
    description='Monitor local file system and sync it with remote server',
    author=META['author'],
    author_email=META['email'],
    url='https://vuk.agency',
    download_url=(url_template % META['version']),
    entry_points={},
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ]
)
