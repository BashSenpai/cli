import codecs
import os.path
from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

# get __version__ from a file
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError('Unable to find version string.')

setup(
    name='senpai-cli',
    version=get_version('src/senpai/__init__.py'),
    description='BashSenpai command line interface',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://BashSenpai.com/',
    author='Bogdan Tatarov',
    author_email='bogdan@tatarov.me',
    license='Apache-2.0',
    install_requires=['requests' 'toml'],
    packages=find_packages(where='src'),
    package_dir = {'': 'src'},
    entry_points=dict(
        console_scripts=['senpai=main:main']
    )
)
