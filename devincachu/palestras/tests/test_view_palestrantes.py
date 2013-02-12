# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django import test
from django.conf import settings
from django.core import management, urlresolvers as u
from django.test import client
from django.views.generic import list
from lxml import html

from .. import models, views


class PalestrantesViewTestCase(test.TestCase):

    def test_deve_herdar_de_ListView(self):
        assert issubclass(views.PalestrantesView, list.ListView)

    def test_template_name_deve_ser_palestrantes(self):
        self.assertEqual("palestrantes.html",
                         views.PalestrantesView.template_name)

    def test_model_deve_ser_Palestrante(self):
        self.assertEqual(models.Palestrante,
                         views.PalestrantesView.model)

    def test_context_object_name_deve_ser_palestrantes(self):
        self.assertEqual("palestrantes",
                         views.PalestrantesView.context_object_name)

    def test_deve_estar_mapeado_para_url_palestrantes(self):
        f = views.PalestrantesView.as_view()
        resolve = u.resolve("/palestrantes/")
        self.assertEqual(f.func_code, resolve.func.func_code)


class TemplatePalestrantesTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def setUp(self):
        factory = client.RequestFactory()
        request = factory.get("/palestrantes")
        view = views.PalestrantesView.as_view()
        self.response = view(request)
        self.response.render()
        self.dom = html.fromstring(self.response.content.decode("utf-8"))

    def test_listagem_de_palestrantes_ul_class(self):
        lis = self.dom.xpath('//ul[@class="palestrantes"]/li')
        self.assertEqual(4, len(lis))

    def test_listagem_de_palestrantes_em_ordem_alfabetica(self):
        lista_esperada = ["Forrest Gump", "Hannibal Lecter",
                          "James Bond", "Vito Corleone"]
        lista_obtida = [p.nome for p in
                        self.response.context_data["palestrantes"]]
        self.assertEqual(lista_esperada, lista_obtida)

    def test_palestrante_com_blog(self):
        xpath = '//ul[@class="palestrantes"]/li/div/a[@href="http://bond.com"]'
        link = self.dom.xpath(xpath)
        self.assertEqual(1, len(link))

    def test_palestrante_sem_blog(self):
        divs = self.dom.xpath('//ul[@class="palestrantes"]/li/div')
        div = divs[3]
        children = div.getchildren()
        c = 0
        for child in children:
            if child.tag == 'a':
                c += 1

        self.assertEqual(1, c)

    def test_palestrante_com_twitter(self):
        xpath = '//ul[@class="palestrantes"]/li/div/' +\
                'a[@href="http://twitter.com/hlecter"]'
        link = self.dom.xpath(xpath)
        self.assertEqual(1, len(link))

    def test_palestrante_com_twitter_comecando_com_arroba(self):
        xpath = '//ul[@class="palestrantes"]/li/div/' +\
                'a[@href="http://twitter.com/vito"]'
        link = self.dom.xpath(xpath)
        self.assertEqual(1, len(link))

    def test_canonical_url_deve_ter_barra_no_final(self):
        esperado = u"%s/palestrantes/" % settings.BASE_URL
        tag = self.dom.xpath('//link[@rel="canonical"]')[0]
        canonical_url = tag.attrib["href"]
        self.assertEqual(esperado, canonical_url)

    def test_nome_de_todos_palestrantes_nos_keywords(self):
        qs = models.Palestrante.objects.filter(listagem=True).order_by("nome")
        esperado = u"dev in cachu, palestrantes, %s" % ", ".join(
            [p.nome for p in qs],
        )
        tag = self.dom.xpath('//meta[@name="keywords"]')[0]
        keywords = tag.attrib["content"]
        self.assertEqual(esperado, keywords)

    def test_description_deve_descrever_a_pagina_de_palestrantes(self):
        esperado = u"Palestrantes do Dev in Cachu 2012"
        tag = self.dom.xpath('//meta[@name="description"]')[0]
        description = tag.attrib["content"]
        self.assertEqual(esperado, description)

    def test_deve_ter_og_title(self):
        esperado = u"Palestrantes do Dev in Cachu 2012"
        tag = self.dom.xpath('//meta[@property="og:title"]')[0]
        title = tag.attrib["content"]
        self.assertEqual(esperado, title)

    def test_deve_ter_og_type_public_figure(self):
        tag = self.dom.xpath('//meta[@property="og:type"]')[0]
        type = tag.attrib["content"]
        self.assertEqual("public_figure", type)

    def test_deve_ter_og_url_para_pagina_de_palestrantes(self):
        esperado = u"%s/palestrantes/" % settings.BASE_URL
        url = self.dom.xpath('//meta[@property="og:url"]')[0].attrib["content"]
        self.assertEqual(esperado, url)

    def test_deve_usar_logomarca_padrao_como_og_image(self):
        esperado = u"%simg/logo-devincachu-facebook.png" % settings.STATIC_URL
        tag = self.dom.xpath('//meta[@property="og:image"]')[0]
        image = tag.attrib["content"]
        self.assertEqual(esperado, image)

    def test_og_description(self):
        esperado = u"Veja mais informações dos palestrantes do " +\
                   u"Dev in Cachu 2012. Conheça quem são e de onde " +\
                   u"vêm os palestrantes dessa edição"
        tag = self.dom.xpath('//meta[@property="og:description"]')[0]
        description = tag.attrib["content"]
        self.assertEqual(esperado, unicode(description))


class TemplatePalestranteSemPalestrantesTestCase(test.TestCase):

    def setUp(self):
        factory = client.RequestFactory()
        request = factory.get("/palestrantes")
        view = views.PalestrantesView.as_view()
        self.response = view(request)
        self.response.render()
        self.dom = html.fromstring(self.response.content)

    def test_nao_deve_renderizar_ul(self):
        ul = self.dom.xpath('//ul[@class="palestrantes"]')
        self.assertEqual(0, len(ul))

    def test_deve_exibir_mensagem_que_nao_ha_palestrantes(self):
        msg = "Não há palestrantes ainda :( " +\
              "Envie sua ideia para contato@devincachu.com.br!"
        self.assertIn(msg, self.response.content)
