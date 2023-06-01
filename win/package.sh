#!/bin/bash
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

export PYTHONPATH="$( pwd -P )/../src"

rm -rf ../dist/win
mkdir -p ../dist/win/build
cp run.py ../dist/win
cp install.iss ../dist/win

pushd ../dist/win > /dev/null
cp -a ../../src/senpai senpai

pyinstaller --clean --onefile \
            --name senpai \
             --noconfirm --log-level ERROR \
            --distpath . --workpath ./build \
            --icon ../../media/app.ico \
            run.py
rm -rf ../dist/build

iscc install.iss
popd > /dev/null
