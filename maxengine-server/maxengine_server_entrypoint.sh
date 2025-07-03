#!/bin/bash
cd /maxtext
python3 -m MaxText.maxengine_server \
/maxtext/MaxText/configs/base.yml \
$@