# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.template import response
from django.test import client

from .. import forms, models, views

MOCKED_CHECKOUT_CODE = "E4B1F4E7D3D3E0D1144ABF9A9D6DFD49"


class ViewInscricaoInscricoesFechadasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        factory = client.RequestFactory()
        request = factory.get("/inscricoes/")
        configuracao = models.Configuracao.objects.get()
        configuracao.status = "fechadas"
        configuracao.save()

        view = views.Inscricao()
        cls.response = view.get(request)

    def test_deve_ter_dicionario_com_templates_para_cada_status(self):
        esperado = {
            u"fechadas": "inscricoes_fechadas.html",
            u"abertas": "inscricoes_abertas.html",
            u"encerradas": "inscricoes_encerradas.html",
        }
        self.assertEqual(esperado, views.Inscricao.templates)

    def test_template(self):
        self.assertEqual(u"inscricoes_fechadas.html",
                         self.response.template_name)

    def test_deve_ter_contexto_vazio(self):
        self.assertEqual({}, self.response.context_data)


class ViewInscricaoInscricoesAbertasTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        factory = client.RequestFactory()
        request = factory.get("/inscricoes/")

        cls.configuracao = models.Configuracao.objects.get()
        cls.configuracao.status = "abertas"
        cls.configuracao.save()

        view = views.Inscricao()
        cls.response = view.get(request)

    def test_template(self):
        self.assertEqual(u"inscricoes_abertas.html",
                         self.response.template_name)

    def test_deve_incluir_instancia_de_ParticipanteForm_no_contexto(self):
        context_data = self.response.context_data
        self.assertIsInstance(context_data["form"], forms.ParticipanteForm)

    def test_deve_incluir_configuracao_no_contexto(self):
        context_data = self.response.context_data
        self.assertEqual(self.configuracao, context_data["configuracao"])


class ViewInscricaoFormularioInvalidoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dados = {
            "nome": "",
            "nome_cracha": "",
            "cidade": "Rio de Janeiro/RJ",
            "sexo": "M",
            "email": "contato@devincachu.com.br",
            "tamanho_camiseta": "",
            "instituicao_ensino": "",
            "empresa": "",
        }
        factory = client.RequestFactory()
        request = factory.post("/inscricoes/", cls.dados)

        view = views.Inscricao()
        cls.response = view.post(request)

    def test_deve_retornar_um_TemplateResponse(self):
        self.assertIsInstance(self.response, response.TemplateResponse)

    def test_deve_renderizar_template_inscricoes_abertas(self):
        self.assertEqual("inscricoes_abertas.html",
                         self.response.template_name)

    def test_formulario_do_contexto_deve_ter_dados_preenchidos(self):
        form = self.response.context_data["form"]
        esperado = sorted(self.dados.items(), key=lambda x: x[0])
        obtido = sorted(form.data.items(), key=lambda x: x[0])
        self.assertEqual(esperado, obtido)


class ViewInscricaoInscricoesAbertasComDadosValidosTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dados = {
            "nome": "Francisco Souza",
            "nome_cracha": "Chico",
            "cidade": "Rio de Janeiro/RJ",
            "sexo": "M",
            "email": "f@souza.cc",
            "tamanho_camiseta": "G",
            "instituicao_ensino": u"Estácio de Sá",
            "empresa": "Globo.com",
        }
        factory = client.RequestFactory()
        request = factory.post("/inscricoes/", cls.dados)
        view = views.Inscricao()
        view.gerar_cobranca = lambda p: MOCKED_CHECKOUT_CODE
        view.enviar_email_falha = lambda c: None
        view.enviar_email_sucesso = lambda c: None
        cls.response = view.post(request)

    @classmethod
    def tearDownClass(cls):
        models.Participante.objects.filter(**cls.dados).delete()

    def test_deve_renderizar_template_inscricao_confirmada(self):
        self.assertEqual("aguardando_pagamento.html",
                         self.response.template_name)

    def test_deve_cadastrar_participante_no_banco_de_dados(self):
        participante = models.Participante.objects.get(**self.dados)
        self.assertEqual(participante.nome, self.dados["nome"])

    def test_deve_criar_checkout_no_banco_com_codigo_e_participante(self):
        participante = models.Participante.objects.get(**self.dados)
        checkout = models.Checkout.objects.get(participante=participante)
        self.assertEqual(MOCKED_CHECKOUT_CODE, checkout.codigo)

    def test_deve_incluir_checkout_no_contexto(self):
        context_data = self.response.context_data
        participante = models.Participante.objects.get(**self.dados)
        checkout = models.Checkout.objects.get(participante=participante)
        self.assertEqual(checkout, context_data["checkout"])


class ViewInscricaoFalhaComunicacaoPagSeguroTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dados = {
            "nome": "Francisco Souza",
            "nome_cracha": "Chico",
            "cidade": "Rio de Janeiro/RJ",
            "sexo": "M",
            "email": "f@souza.cc",
            "tamanho_camiseta": "G",
            "instituicao_ensino": u"Estácio de Sá",
            "empresa": "Globo.com",
        }
        factory = client.RequestFactory()
        request = factory.post("/inscricoes/", cls.dados)
        view = views.Inscricao()
        view.gerar_cobranca = lambda p: None
        cls.response = view.post(request)

    def test_deve_renderizar_template_falha_comunicacao_pagseguro(self):
        self.assertEqual(u"falha_comunicacao_pagseguro.html",
                         self.response.template_name)

    def test_deve_incluir_participante_no_contexto(self):
        participante = models.Participante.objects.get(**self.dados)
        context_data = self.response.context_data
        self.assertEqual(participante, context_data["participante"])
