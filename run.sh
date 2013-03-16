#!/bin/sh

export `circusctl options gunicorn-devincachu | grep ^env: | cut -f2 -d' ' | sed -e 's/,/\nexport /g'`
export PATH="$HOME/devincachu2013/env/bin:$PATH"
exec $*
