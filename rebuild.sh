#!/bin/sh
virtualenv venv
. venv/bin/activate
sh -x reinstall.sh
