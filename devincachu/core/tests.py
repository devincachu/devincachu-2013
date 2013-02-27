# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.conf import settings
from django.test import client
from django.utils import safestring

from . import processors
from .templatetags import devincachu


class ProcessorsTestCase(unittest.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")

    def test_deve_retornar_dicionario_com_BASE_URL(self):
        esperado = {u"BASE_URL": settings.BASE_URL}
        self.assertEqual(esperado, processors.get_base_url(self.request))

    def test_deve_estar_registrado_nos_CONTEXT_PROCESSORS(self):
        self.assertIn(
            "devincachu.core.processors.get_base_url",
            settings.TEMPLATE_CONTEXT_PROCESSORS,
        )


class MarkdownTestCase(unittest.TestCase):

    def test_deve_aceitar_raw_html(self):
        input = u"""#Something

<a href="http://2013.devincachu.com.br">visite o dev in cachu</a>"""
        esperado = u"<h1>Something</h1>\n<p>" +\
                   u"<a href=\"http://2013.devincachu.com.br\">visite o " +\
                   u"dev in cachu</a></p>"
        obtido = devincachu.markdown(input)
        self.assertEqual(esperado, obtido)

    def test_deve_estar_registrado(self):
        self.assertEqual(devincachu.markdown,
                         devincachu.register.filters["markdown"])

    def test_deve_ser_safe(self):
        obtido = devincachu.markdown("#alguma coisa")
        self.assertIsInstance(obtido, safestring.SafeText)
