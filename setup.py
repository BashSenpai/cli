from setuptools import setup, find_packages

setup(
    name='senpai-cli',
    version='0.70a',
    description='BashSenpai command line interface',
    url='https://BashSenpai.com/',
    author='Bogdan Tatarov',
    author_email='bogdan@tatarov.me',
    license='Apache-2.0',
    install_requires=['requests' 'toml'],
    packages=find_packages(where='src'),
    package_dir = {'': 'src'},
    entry_points=dict(
        console_scripts=['senpai=senpai:main']
    )
)
