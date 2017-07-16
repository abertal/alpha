#!/bin/bash
java -Dnu.validator.servlet.filterfile=message-filters.txt -cp vnu.jar nu.validator.servlet.Main 8888 &
