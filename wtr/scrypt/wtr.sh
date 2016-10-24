#!/bin/bash

a=$(dirname $0)
a+="/wtr_script.pyc"

python2 $a $@
