# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# This code is based on work previously done on pythonbrasil8 website:
#    https://raw.github.com/pythonbrasil/pythonbrasil8/master/pagseguro_transaction.py

import datetime

import requests
import xmltodict

from django.conf import settings
from django.core.management import base

from devincachu.inscricao import models, views


class Command(base.BaseCommand):
    args = u"<quantidade_de_dias>"
    help = u"Obtém transações do PagSeguro e atualiza informações no banco de dados."

    def get_transactions(self, initial_date, final_date):
        """Get all transactions in the interval

        If more than one page is needed, it automatically gets ALL the pages.
        `initial_date` and `final_date` should be in format
        `YYYY-MM-DDTHH:MM:SS`.
        PagSeguro"s API documentation says it must be `YYYY-MM-DDTHH:MM:SS.sz`,
        where "s" is microseconds and "z" is timezone, but it is not needed and
        it fails in some cases!
        """
        page = 1
        max_results = 100
        finished = False
        parameters = {"initialDate": initial_date, "finalDate": final_date,
                      "maxPageResults": max_results, "email": settings.PAGSEGURO["email"],
                      "token": settings.PAGSEGURO["token"]}
        transactions = []
        while not finished:
            parameters["page"] = page
            response = requests.get(settings.PAGSEGURO_TRANSACTIONS, params=parameters)
            data = xmltodict.parse(response.text.encode("iso-8859-1"))
            result = data["transactionSearchResult"]
            if int(result["resultsInThisPage"]) > 0:
                new_transactions = result["transactions"]["transaction"]
                if type(new_transactions) is not list:  # only one returned
                    new_transactions = [new_transactions]
                transactions.extend(new_transactions)
            total_pages = int(result["totalPages"])
            if page < total_pages:
                page += 1
            elif page == total_pages:
                finished = True
        return transactions

    def handle(self, *args, **kwargs):
        qt_dias = 1
        if len(args) > 0:
            qt_dias = int(args[0])
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=qt_dias)
        start = yesterday.strftime("%Y-%m-%dT%H:%M:%S-02:00")
        end = now.strftime("%Y-%m-%dT%H:%M:%S-02:00")
        whole_transactions = self.get_transactions(start, end)

        paid = [t for t in whole_transactions
                if "reference" in t
                and t["status"] in ("3", "4")]
        for transaction in paid:
            notificacao = views.Notificacao()
            subscription_id = transaction["reference"]
            participante = models.Participante.objects.get(pk=subscription_id)
            if participante.status not in (u"CONFIRMADO", u"CARAVANA"):
                participante.status = u"CONFIRMADO"
                if transaction["grossAmount"] not in ("35.00", "50.00"):
                    participante.status = u"CARAVANA"
                participante.save()
                notificacao.enviar_email_confirmacao(participante)
