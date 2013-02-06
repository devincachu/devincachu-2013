# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.conf import settings
from django.test import client

from . import processors


class ProcessorsTestCase(unittest.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")

    def test_deve_retornar_dicionario_com_BASE_URL(self):
        esperado = {u"BASE_URL": settings.BASE_URL}
        self.assertEquals(esperado, processors.get_base_url(self.request))

    def test_deve_estar_registrado_nos_CONTEXT_PROCESSORS(self):
        self.assertIn(
            "devincachu.core.processors.get_base_url",
            settings.TEMPLATE_CONTEXT_PROCESSORS,
        )
