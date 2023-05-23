from setuptools import setup, find_packages

from src.senpai.main import get_version


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='senpai-cli',
    version=get_version(),
    description='BashSenpai command-line interface',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://BashSenpai.com/',
    author='Bogdan Tatarov',
    author_email='bogdan@tatarov.me',
    license='Apache-2.0',
    install_requires=['requests', 'toml'],
    packages=find_packages(where='src'),
    package_dir = {'': 'src'},
    entry_points=dict(
        console_scripts=['senpai=senpai:main']
    )
)
