# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.conf import settings
from django.core import management, urlresolvers
from django.template import response
from django.test import client
from django.views.generic import base
from lxml import html

from .. import views


class IndexViewTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "destaques.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")
        self.view = views.IndexView()

    def test_view_deve_herdar_de_View(self):
        assert issubclass(views.IndexView, base.View)

    def test_deve_responder_pela_url_raiz(self):
        f = views.IndexView.as_view()
        r = urlresolvers.resolve('/')
        self.assertEqual(f.func_name, r.func.func_name)

    def test_metodo_obter_destaque_deve_trazer_no_maximo_14_destaques(self):
        destaques = self.view.obter_destaques()
        self.assertEqual(14, len(destaques))

    def test_metodo_obter_destaque_deve_trazer_destaques_mais_recentes(self):
        esperado = [
            u"Bill Gates confirma participação no Dev in Cachu 2021",
            u"Bill Gates confirma participação no Dev in Cachu 2020",
            u"Bill Gates confirma participação no Dev in Cachu 2019",
            u"Bill Gates confirma participação no Dev in Cachu 2018",
            u"Bill Gates confirma participação no Dev in Cachu 2017",
            u"Bill Gates confirma participação no Dev in Cachu 2016",
            u"Bill Gates confirma participação no Dev in Cachu 2015",
            u"Bill Gates confirma participação no Dev in Cachu 2014",
            u"Palestra sobre C++",
            u"Palestra sobre Java",
            u"Palestra sobre C#",
            u"Palestra sobre Python",
            u"Bill Gates confirma participação no Dev in Cachu 2013",
            u"Bill Gates confirma participação no Dev in Cachu 2012",
        ]

        destaques = [d.titulo for d in self.view.obter_destaques()]
        self.assertEqual(esperado, destaques)

    def test_metodo_get_deve_retornar_TemplateResponse(self):
        r = self.view.get(self.request)
        self.assertIsInstance(r, response.TemplateResponse)

    def test_metodo_get_deve_renderizar_template_index(self):
        r = self.view.get(self.request)
        self.assertEqual("index.html", r.template_name)

    def test_metodo_get_deve_colocar_destaques_no_contexto(self):
        destaques = list(self.view.obter_destaques())
        r = self.view.get(self.request)
        self.assertEqual(destaques, list(r.context_data['destaques']))

    def test_deve_ter_canonical_url_da_home(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = "%s/" % settings.BASE_URL
        obtido = dom.xpath('//link[@rel="canonical"]')[0].attrib["href"]
        self.assertEqual(esperado, obtido)

    def test_meta_keywords(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"devincachu, dev in cachu 2013, evento de " +\
                   u"informática, desenvolvimento de software, " +\
                   u"cachoeiro de itapemirim"
        obtido = dom.xpath('//meta[@name="keywords"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_meta_description(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"Dev in Cachu 2013 - evento sobre desenvolvimento " +\
                   u"de software no sul do Espírito Santo"
        obtido = dom.xpath('//meta[@name="description"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_og_title_deve_ter_nome_e_edicao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"Dev in Cachu 2013"
        obtido = dom.xpath('//meta[@property="og:title"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_og_type_deve_ser_website(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"website"
        obtido = dom.xpath('//meta[@property="og:type"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_og_url_deve_ser_BASE_URL_com_barra_no_final(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"%s/" % settings.BASE_URL
        obtido = dom.xpath('//meta[@property="og:url"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_og_image_deve_ser_logomarca_padrao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"%simg/devincachu-facebook.png" % settings.STATIC_URL
        obtido = dom.xpath('//meta[@property="og:image"]')[0].attrib["content"]
        self.assertEqual(esperado, obtido)

    def test_og_description_deve_trazer_descricao_do_evento(self):
        r = self.view.get(self.request)
        r.render()
        dom = html.fromstring(r.content.decode("utf-8"))
        esperado = u"Maior evento de desenvolvimento de software " +\
                   u"do Espírito Santo. Organizado com o objetivo de " +\
                   u"difundir técnicas e práticas de desenvolvimento de " +\
                   u"software, trazendo diversos temas."
        tag = dom.xpath('//meta[@property="og:description"]')[0]
        self.assertEqual(esperado, tag.attrib["content"])


class IndexViewSemDados(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        factory = client.RequestFactory()
        self.request = factory.get("/")
        self.view = views.IndexView()

    def test_metodo_obter_destaques_ausencia_de_dados(self):
        self.assertEqual(0, len(self.view.obter_destaques()))
