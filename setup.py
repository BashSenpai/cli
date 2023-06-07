# Copyright 2023 Bogdan Tatarov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

from senpai.main import get_version


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
    install_requires=('requests', 'toml'),
    packages=find_packages(),
    entry_points=dict(
        console_scripts=['senpai=senpai.main:main']
    )
)
