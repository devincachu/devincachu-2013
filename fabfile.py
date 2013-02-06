# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

from fabric.api import cd, env, run, settings

env.root = os.path.dirname(__file__)
env.app = os.path.join(env.root, 'devincachu')
env.base_dir = '/home/devincachu'
env.project_root = os.path.join(env.base_dir, 'devincachu2013')
env.virtualenv = os.path.join(env.project_root, 'env')
env.shell = '/bin/sh -c'
env.hosts = ['2013.devincachu.com.br']
env.user = 'devincachu'


def update_app():
    run('([ -d %(project_root)s ] && ' +
        'cd %(project_root)s && git fetch origin && ' +
        'git rebase origin/master) || (cd %(base_dir)s && ' +
        'git clone git://github.com/devincachu/devincachu-2013.git ' +
        '%(project_root)s)' % env)


def create_virtualenv_if_need():
    run('[ -d %(virtualenv)s ] || virtualenv %(virtualenv)s' % env)


def pip_install():
    run('CFLAGS=-I/usr/local/include LDFLAGS=-L/usr/local/lib ' +
        '%(virtualenv)s/bin/pip install -r ' +
        '%(project_root)s/requirements_env.txt' % env)


def collect_static_files():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/python manage.py collectstatic ' +
            '-v 0 --noinput' % env)


def syncdb():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/python manage.py syncdb --noinput' % env)


def start_gunicorn():
    with cd(env.project_root):
        run('%(virtualenv)s/bin/gunicorn --pid=gunicorn.pid --daemon ' +
            '--workers=3 --access-logfile=devincachu_access.log ' +
            '--error-logfile=devincachu_error.log --bind=127.0.0.1:8989 ' +
            'devincachu.wsgi' % env)


def stop_gunicorn():
    with settings(warn_only=True):
        pid = run('cat %(project_root)s/gunicorn.pid' % env)
        run('kill -TERM %s' % pid)


def graceful_gunicorn():
    with settings(warn_only=True):
        pid = run('cat %(project_root)s/gunicorn.pid' % env)
        run('kill -HUP %s' % pid)


def restart_nginx():
    run("su -m root -c '/usr/local/etc/rc.d/nginx restart'")


def clean():
    run("su -m root -c " +
        "'rm -rf /usr/local/etc/nginx/cache/data/devincachu2013/*'")
    restart_nginx()


def createsuperuser():
    with cd(env.project_root):
        run("%(virtualenv)s/bin/python manage.py createsuperuser" % env)


def deploy():
    update_app()
    create_virtualenv_if_need()
    pip_install()
    collect_static_files()
