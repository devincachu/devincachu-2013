# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

from fabric.api import cd, env, run

env.root = os.path.dirname(__file__)
env.app = os.path.join(env.root, 'devincachu')
env.base_dir = '/home/devincachu'
env.project_root = os.path.join(env.base_dir, 'devincachu2013')
env.virtualenv = os.path.join(env.project_root, 'env')
env.shell = '/bin/sh -c'
env.hosts = ['2013.devincachu.com.br']
env.user = 'devincachu'


def update_app():
    run(('([ -d %(project_root)s ] && ' % env +
        'cd %(project_root)s && git fetch origin && ' +
        'git rebase origin/master) || (cd %(base_dir)s && ' +
        'git clone git://github.com/devincachu/devincachu-2013.git ' +
        '%(project_root)s)') % env)


def create_virtualenv_if_need():
    run('[ -d %(virtualenv)s ] || virtualenv %(virtualenv)s' % env)


def pip_install():
    run(('CFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib ' +
         '%(virtualenv)s/bin/pip install -r ' +
         '%(project_root)s/requirements_env.txt') % env)


def collect_static_files():
    with cd(env.project_root):
        run(('%(virtualenv)s/bin/python manage.py collectstatic ' +
             '-v 0 --noinput') % env)


def syncdb():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/python manage.py syncdb --noinput' % env)


def start_gunicorn():
    run('circusctl start gunicorn-devincachu')


def stop_gunicorn():
    run('circusctl stop gunicorn-devincachu')


def restart_gunicorn():
    run('circusctl restart gunicorn-devincachu')


def restart_nginx():
    run("su -c 'restart nginx' -")


def clean():
    run("su -c " +
        "'rm -rf /opt/cache/data/devincachu2013/*' -")
    restart_nginx()


def deploy():
    update_app()
    create_virtualenv_if_need()
    pip_install()
    collect_static_files()
