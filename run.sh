#!/bin/sh -e

my_dir=`dirname $0`
cd $my_dir
export `circusctl options gunicorn-devincachu | grep ^env: | cut -f2 -d' ' | sed -e 's/,/\nexport /g'`
export PATH="$PWD/env/bin:$PATH"
exec $*
