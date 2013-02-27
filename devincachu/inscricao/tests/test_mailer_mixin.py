# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import time

from django.core import mail
from django import test

from .. import views


class MailerMixinTestCase(test.TestCase):

    def setUp(self):
        mail.outbox = []

    def test_enviar_email_deve_enviar_email_com_parametros_passados(self):
        mailer = views.MailerMixin()
        mailer.enviar_email(u"Assunto", u"Corpo", ["eu@gmail.com"])
        time.sleep(1)
        email = mail.outbox[0]
        self.assertEqual(u"Assunto", email.subject)
        self.assertEqual(u"Corpo", email.body)
        self.assertEqual(["eu@gmail.com"], email.to)

    def test_enviar_email_deve_enviar_email_como_contato_at_devincachu(self):
        mailer = views.MailerMixin()
        mailer.enviar_email(u"Assunto", u"Corpo", ["eu@gmail.com"])
        time.sleep(1)
        email = mail.outbox[0]
        self.assertEqual("contato@devincachu.com.br", email.from_email)
