#!/bin/bash
set -ex
wget https://github.com/validator/validator/releases/download/18.3.0/vnu.jar_18.3.0.zip -O ./vnu.jar.zip
unzip -op vnu.jar.zip dist/vnu.jar > vnu.jar
