# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.conf import settings
from django.core import management
from django.test import client
from django.views.generic import list as vlist
from lxml import html

from .. import models, views


class ProgramacaoViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes", "palestras", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/programacao")

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.ProgramacaoView, vlist.ListView)

    def test_deve_usar_model_Palestra(self):
        self.assertEqual(models.Palestra, views.ProgramacaoView.model)

    def test_deve_ter_context_object_name_para_palestras(self):
        self.assertEqual("palestras", views.ProgramacaoView.context_object_name)

    def test_deve_trazer_palestras_no_contexto_ordenadas_pelo_horario_de_inicio(self):
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        palestras = response.context_data["palestras"]
        titulos_esperados = [u"Recepção e credenciamento", u"Escalando aplicações Django", u"Arquitetura escalável de aplicação de alto desempenho", u"Almoço"]
        titulos_obtidos = [p.titulo for p in palestras]
        self.assertEqual(titulos_esperados, titulos_obtidos)

    def test_nao_deve_incluir_tags_html_no_title_da_grade_de_programacao(self):
        palestra = models.Palestra.objects.get(pk=1)
        palestra.descricao = u"[Oi](http://www.google.com.br), você vem sempre aqui?"
        palestra.save()

        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()

        dom = html.fromstring(response.content.decode("utf-8"))
        title_obtido = dom.xpath('//a[@href="%s"]' % palestra.get_absolute_url())[0].attrib["title"]
        self.assertEqual(u"Oi, você vem sempre aqui?", unicode(title_obtido))

    def test_deve_definir_canonical_url(self):
        esperado = "%s/programacao/" % settings.BASE_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content)
        self.assertEqual(esperado, dom.xpath('//link[@rel="canonical"]')[0].attrib["href"])

    def test_deve_ter_meta_keywords(self):
        esperado = u"devincachu, dev in cachu 2012, palestras, programação, desenvolvimento de software"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@name="keywords"]')[0].attrib["content"]
        self.assertEqual(esperado, unicode(obtido))

    def test_deve_ter_meta_description(self):
        esperado = u"Grade de programação do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@name="description"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_deve_ter_og_description(self):
        esperado = u"Conheça as atrações e os convidados especiais do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@property="og:description"]')[0].attrib["content"]
        self.assertEqual(esperado, unicode(obtido))

    def test_deve_ter_og_title_descrevendo_a_pagin(self):
        esperado = u"Grade de programação do Dev in Cachu 2012"
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@property="og:title"]')[0].attrib["content"]
        self.assertEqual(esperado, unicode(obtido))

    def test_deve_ter_og_type_activity(self):
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@property="og:type"]')[0].attrib["content"]
        self.assertEqual(u"activity", unicode(obtido))

    def test_deve_ter_og_url(self):
        esperado = "%s/programacao/" % settings.BASE_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@property="og:url"]')[0].attrib["content"]
        self.assertEqual(esperado, unicode(obtido))

    def test_deve_ter_og_image_apontando_para_logo_do_devincachu(self):
        esperado = "%simg/logo-devincachu-facebook.png" % settings.STATIC_URL
        view = views.ProgramacaoView.as_view()
        response = view(self.request)
        response.render()
        dom = html.fromstring(response.content.decode("utf-8"))
        obtido = dom.xpath('//meta[@property="og:image"]')[0].attrib["content"]
        self.assertEqual(esperado, unicode(obtido))
