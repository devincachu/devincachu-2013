# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCES_DIRECTORY = os.path.abspath(os.path.join(ROOT, "..", "resources"))

DEBUG = int(os.environ.get("DEVINCACHU_DEBUG", 1)) != 0
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = not DEBUG

ADMINS = (
    # ("Your Name", "your_email@example.com"),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DEVINCACHU_DB_NAME", "devincachu"),
        "USER": os.environ.get("DEVINCACHU_DB_USER", "root"),
        "PASSWORD": os.environ.get("DEVINCACHU_DB_PASSWORD", ""),
        "HOST": os.environ.get("DEVINCACHU_DB_HOST", "localhost"),
        "PORT": os.environ.get("DEVINCACHU_DB_PORT", 3306),
    }
}

TIME_ZONE = "America/Sao_Paulo"

LANGUAGE_CODE = "pt-br"

SITE_ID = 1

USE_I18N = True

USE_L10N = True

ALLOWED_HOSTS = (
    "2013.devincachu.com.br",
)

MEDIA_ROOT = os.path.join(ROOT, "media")
MEDIA_URL = os.environ.get("DEVINCACHU_MEDIA_URL", "/media/")
BASE_URL = "http://2013.devincachu.com.br"
ROAN_PURGE_URL = "%s/purge" % BASE_URL

STATIC_ROOT = os.path.join(ROOT, "static")
STATIC_URL = os.environ.get("DEVINCACHU_STATIC_URL", "/static/")
STATICFILES_DIRS = (
    os.path.join(ROOT, "static_files"),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

SECRET_KEY = os.environ.get("DEVINCACHU_SECRET_KEY", "not-secret")

TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
    "django.template.loaders.eggs.Loader",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "devincachu.core.processors.get_base_url",
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
)

ROOT_URLCONF = "devincachu.urls"

TEST_RUNNER = 'devincachu.runner.DiscoveryRunner'

COMPRESS_CSS_FILTERS = (
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
)

COMPRESS_JS_FILTERS = (
    "compressor.filters.jsmin.SlimItFilter",
)

KEEP_COMMENTS_ON_MINIFYING = True
EXCLUDE_FROM_MINIFYING = ("^admin/",)

TEMPLATE_DIRS = (
    os.path.join(ROOT, "templates"),
)

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.markup",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.flatpages",
    "compressor",
    "devincachu.core",
    "devincachu.destaques",
    "devincachu.palestras",
    "devincachu.inscricao",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        },
        "django_error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "devincachu_djerror.log",
            "maxBytes": "1024",
            "backupCount": "1",
            "formatter": "verbose",
        },
        "inscricoes": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "inscricoes.log",
            "maxBytes": "2048",
            "backupCount": "3",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["django_error"],
            "level": "ERROR",
            "propagate": True,
        },
        "devincachu.inscricoes": {
            "handlers": ["inscricoes"],
            "level": "INFO",
            "propagate": False,
        }
    }
}

PAGSEGURO = {
    "email": os.environ.get("DEVINCACHU_PS_EMAIL", "ps@devincachu.com.br"),
    "charset": "UTF-8",
    "token": os.environ.get("DEVINCACHU_PS_TOKEN", "not-secret"),
    "currency": "BRL",
    "itemId1": "0001",
    "itemDescription1": u"Inscrição no Dev in Cachu 2013",
    "itemQuantity1": 1,
}

PAGSEGURO_BASE = "https://ws.pagseguro.uol.com.br/v2"
PAGSEGURO_CHECKOUT = "%s/checkout" % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS = "%s/transactions" % PAGSEGURO_BASE
PAGSEGURO_TRANSACTIONS_NOTIFICATIONS = "%s/notifications" % \
                                       PAGSEGURO_TRANSACTIONS

EMAIL_HOST = os.environ.get("DEVINCACHU_EMAIL_HOST")
EMAIL_PORT = os.environ.get("DEVINCACHU_EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("DEVINCACHU_EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("DEVINCACHU_EMAIL_PASSWORD")
EMAIL_USE_TLS = True
