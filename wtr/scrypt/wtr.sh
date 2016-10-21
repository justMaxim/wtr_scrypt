#!/bin/bash

a=$(dirname $0)
a+="/wtr_scrypt.pyc"

python2 $a $@
