#!/usr/bin/env bash

command -v npm >/dev/null 2>&1 || { echo >&2 "npm not installed.  Aborting."; exit 1; }
cd src/
npm run build
cd ../
if [ -d app/static ]; then
    rm -rf app/static
fi
mv build/* app/
mkdir app/static/img/
mv app/favicon.ico app/static/img/
mv app/index.html app/templates/index.html
rmdir build/