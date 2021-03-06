# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.core import management
from django.db import models as django_models

from .. import models


class CertificadoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = models.Certificado._meta.get_all_field_names()

    def test_deve_ter_campo_apontando_para_o_participante(self):
        self.assertIn("participante", self.field_names)

    def test_participante_deve_ser_uma_FK(self):
        field = models.Certificado._meta.get_field_by_name("participante")[0]
        self.assertIsInstance(field, django_models.ForeignKey)

    def test_participante_deve_apontar_para_Participante(self):
        field = models.Certificado._meta.get_field_by_name("participante")[0]
        self.assertEqual(models.Participante, field.related.parent_model)

    def test_deve_ter_campo_codigo(self):
        self.assertIn("codigo", self.field_names)

    def test_codigo_deve_ser_CharField(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("codigo")
        self.assertIsInstance(field, django_models.CharField)

    def test_codigo_deve_ter_no_maximo_14_caracteres(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("codigo")
        self.assertEqual(14, field.max_length)

    def test_codigo_deve_ser_unique(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("codigo")
        self.assertTrue(field.unique)

    def test_deve_ter_campo_hash(self):
        self.assertIn("hash", self.field_names)

    def test_hash_deve_ser_do_tipo_CharField(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("hash")
        self.assertIsInstance(field, django_models.CharField)

    def test_hash_deve_ter_no_maximo_100_caracteres(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("hash")
        self.assertEqual(100, field.max_length)

    def test_hash_deve_ser_unique(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("hash")
        self.assertTrue(field.unique)

    def test_deve_ter_campo_horas(self):
        self.assertIn("horas", self.field_names)

    def test_horas_deve_ser_integer(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("horas")
        self.assertIsInstance(field, django_models.IntegerField)

    def test_horas_deve_ser_8_por_padrao(self):
        field, _, _, _ = models.Certificado._meta.get_field_by_name("horas")
        self.assertEqual(8, field.default)

    def test_unicode_deve_retornar_codigo_e_nome_do_participante(self):
        p = models.Participante(nome=u"Francisco Souza")
        c = models.Certificado(codigo=u"2012080439", participante=p)
        self.assertEqual(u"2012080439 (Francisco Souza)", unicode(c))


class GeracaoCertificadoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "certificados.yaml", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", interactive=False, verbosity=0)

    def test_gerar_certificado_cria_certificado(self):
        participante = models.Participante.objects.get(pk=3)
        certificado = models.Certificado.gerar_certificado(participante)
        self.assertIsNotNone(certificado.pk)
        self.assertEqual(8, certificado.horas)
        self.assertEqual(participante, certificado.participante)

    def test_gerar_certificado_retorna_None_para_participante_ausente(self):
        participante = models.Participante.objects.get(pk=1)
        certificado = models.Certificado.gerar_certificado(participante)
        self.assertIsNone(certificado)
