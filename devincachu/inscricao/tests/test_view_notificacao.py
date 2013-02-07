# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.test import client
from django.views.generic import base

from .. import models, views


class NotificacaoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dados = {
            "notificationCode": "766B9C-AD4B044B04DA-77742F5FA653-E1AB24",
            "notificationType": "transation",
        }

        cls.factory = client.RequestFactory()
        cls.request = cls.factory.post("/notificacao/", cls.dados)

    def setUp(self):
        self.participante = models.Participante.objects.create(
            nome=u"Francisco Souza",
            sexo=u"M",
            email=u"francisco@franciscosouza.net",
            tamanho_camiseta=u"G",
        )

    def tearDown(self):
        self.participante.delete()

    def test_deve_herdar_de_View(self):
        assert issubclass(views.Notificacao, base.View)

    def test_nao_deve_implementar_metodo_get(self):
        self.assertFalse(hasattr(views.Notificacao, "get"))

    def test_deve_retornar_200(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (3, self.participante.pk)
        view.enviar_email_confirmacao = lambda p: None
        response = view.post(self.request)
        self.assertEqual(200, response.status_code)

    def test_deve_retornar_OK(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (3, self.participante.pk)
        view.enviar_email_confirmacao = lambda p: None
        response = view.post(self.request)
        self.assertEqual("OK", response.content)

    def test_apenas_retornar_OK_quando_der_erro_no_response(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (None, None)
        response = view.post(self.request)
        self.assertEqual("OK", response.content)

    def test_apenas_retornar_OK_quando_status_for_diferente_de_3_e_7(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (2, self.participante.pk)
        view.enviar_email_confirmacao = lambda p: None
        response = view.post(self.request)
        self.assertEqual("OK", response.content)

    def test_deve_retornar_OK_mesmo_se_nao_tiver_notificationCode(self):
        request = self.factory.post("/notificacao/", {})
        view = views.Notificacao()
        response = view.post(request)
        self.assertEqual("OK", response.content)

    def test_status_para_transacao_confirmada(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (3, self.participante.pk)
        view.enviar_email_confirmacao = lambda p: None
        view.post(self.request)

        participante = models.Participante.objects.get(pk=self.participante.pk)
        self.assertEqual(u"CONFIRMADO", participante.status)

    def test_status_para_transacao_cancelada(self):
        view = views.Notificacao()
        view.consultar_transacao = lambda x: (7, self.participante.pk)
        view.enviar_email_cancelamento = lambda p: None
        view.post(self.request)

        participante = models.Participante.objects.get(pk=self.participante.pk)
        self.assertEqual(u"CANCELADO", participante.status)
