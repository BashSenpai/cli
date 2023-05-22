#!/bin/bash
TASKDIR="$( cd "$(dirname "$0")/" ; pwd -P )"
BASEDIR="$( cd "$(dirname "$0")/../../../" ; pwd -P )"

source .venv/bin/activate
export PYTHONPATH="$( pwd -P )/src"

pushd "$PYTHONPATH" > /dev/null
python -c "import senpai; senpai.main()" $@
popd > /dev/null
