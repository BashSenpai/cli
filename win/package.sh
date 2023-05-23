#!/bin/bash

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
