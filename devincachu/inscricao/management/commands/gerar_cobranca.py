# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import copy
import sys

import requests

from django.conf import settings
from django.core.management import base
from django.template import loader
from lxml import etree

from devincachu.inscricao import models, views


class Command(base.BaseCommand, views.MailerMixin):

    def enviar_email_cobranca(self, checkout, sufixo):
        conteudo = loader.render_to_string("email_aguardando.html",
                                           {"checkout": checkout})
        assunto = u"[Dev in Cachu 2013] Inscrição recebida - %s" % sufixo
        self.enviar_email(assunto, conteudo, [checkout.participante.email])

    def gerar_cobranca(self, participante, sufixo, valor):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        payload = copy.deepcopy(settings.PAGSEGURO)
        payload["itemDescription1"] += "- %s" % sufixo
        payload["itemAmount1"] = "%.2f" % valor
        payload["reference"] = "%s" % participante.pk
        response = requests.post(settings.PAGSEGURO_CHECKOUT,
                                 data=payload, headers=headers)
        if response.ok:
            dom = etree.fromstring(response.content)
            codigo_checkout = dom.xpath("//code")[0].text
            return codigo_checkout

    def handle(self, *args, **kwargs):
        valor = int(sys.stdin.readline().strip("\n"))
        sufixo = sys.stdin.readline().strip("\n")
        emails = [l.strip("\n") for l in sys.stdin.readlines()]
        for email in emails:
            print u"Gerando cobrança para %s... " % email,
            try:
                participante = models.Participante.objects.get(email=email)
            except models.Participante.DoesNotExist:
                print u"NAO ESTA INSCRITO NO SITE"
                continue
            cod_checkout = self.gerar_cobranca(participante, sufixo, valor)
            if cod_checkout is None:
                print u"FALHOU"
                continue
            checkout = models.Checkout.objects.create(
                codigo=cod_checkout,
                participante=participante,
            )
            self.enviar_email_cobranca(checkout, sufixo)
            print u"OK"
