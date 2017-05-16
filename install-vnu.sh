#!/bin/bash
set -ex
wget https://github.com/validator/validator/releases/download/17.3.0/vnu.jar_17.3.0.zip -O ./vnu.jar.zip
unzip -op vnu.jar.zip dist/vnu.jar > vnu.jar
