# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.core import management
from django.db import models as django_models

from .. import models


class ModelPalestraTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        management.call_command("loaddata", "palestrantes",
                                "palestras", verbosity=0)
        cls.field_names = models.Palestra._meta.get_all_field_names()

    @classmethod
    def tearDownClass(cls):
        management.call_command("flush", verbosity=0, interactive=False)

    def test_model_palestra_deve_ter_titulo(self):
        self.assertIn("titulo", self.field_names)

    def test_titulo_deve_ser_CharField(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_titulo_deve_ter_no_maximo_150_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertEqual(150, field.max_length)

    def test_titulo_deve_ter_verbose_name_com_caractere_especial(self):
        field = models.Palestra._meta.get_field_by_name("titulo")[0]
        self.assertEqual(u"Título", field.verbose_name)

    def test_model_palestra_deve_ter_slug(self):
        self.assertIn("slug", self.field_names)

    def test_slug_deve_ser_SlugField(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertIsInstance(field, django_models.SlugField)

    def test_slug_deve_ter_no_maximo_150_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertEqual(150, field.max_length)

    def test_slug_deve_ser_unico(self):
        field = models.Palestra._meta.get_field_by_name("slug")[0]
        self.assertTrue(field.unique)

    def test_model_palestra_deve_ter_descricao(self):
        self.assertIn("descricao", self.field_names)

    def test_descricao_deve_ser_CharField(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_descricao_deve_ter_no_maximo_2000_caracteres(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertEqual(2000, field.max_length)

    def test_descricao_deve_ter_verbose_name_com_caracteres_especiais(self):
        field = models.Palestra._meta.get_field_by_name("descricao")[0]
        self.assertEqual(u"Descrição", field.verbose_name)

    def test_model_palestra_deve_ter_hora_de_inicio(self):
        self.assertIn("inicio", self.field_names)

    def test_inicio_deve_ser_do_tipo_TimeField(self):
        field = models.Palestra._meta.get_field_by_name("inicio")[0]
        self.assertIsInstance(field, django_models.TimeField)

    def test_inicio_deve_ter_verbose_name_descritivo(self):
        field = models.Palestra._meta.get_field_by_name("inicio")[0]
        self.assertEqual(u"Horário de início", field.verbose_name)

    def test_model_palestra_deve_ter_hora_de_termino(self):
        self.assertIn("termino", self.field_names)

    def test_termino_deve_ser_do_tipo_TimeField(self):
        field = models.Palestra._meta.get_field_by_name("termino")[0]
        self.assertIsInstance(field, django_models.TimeField)

    def test_termino_dve_ter_verbose_name_descritivo(self):
        field = models.Palestra._meta.get_field_by_name("termino")[0]
        self.assertEqual(u"Horário de término", field.verbose_name)

    def test_model_palestra_deve_ter_campo_palestrantes(self):
        self.assertIn("palestrantes", self.field_names)

    def test_palestrantes_deve_ser_um_ManyToManyField(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertIsInstance(field, django_models.ManyToManyField)

    def test_palestrantes_deve_apontar_para_model_Palestrante(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertEqual(models.Palestrante, field.related.parent_model)

    def test_palestrantes_deve_aceitar_blank(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertTrue(field.blank)

    def test_palestrantes_deve_ter_related_name_palestras(self):
        field = models.Palestra._meta.get_field_by_name("palestrantes")[0]
        self.assertEqual(u"palestras", field.rel.related_name)

    def test_nomes_palestrantes(self):
        palestra = models.Palestra.objects.get(pk=1)
        self.assertEqual(u"Hannibal Lecter e Vito Corleone",
                         palestra.nomes_palestrantes())

    def test_Palestra_repr(self):
        palestra = models.Palestra(titulo=u"Testando aplicativos web")
        self.assertEqual(u'<Palestra: Testando aplicativos web>',
                         repr(palestra))

    def test_deve_exibir_titulo_como_unicode(self):
        palestra = models.Palestra(titulo=u"Testando aplicações web")
        self.assertEqual(palestra.titulo, unicode(palestra))

    def test_get_absolute_url_com_palestrante(self):
        palestra = models.Palestra.objects.get(pk=1)
        url_esperada = "/programacao/hannibal-lecter/vito-corleone/%s/" %\
                       palestra.slug
        self.assertEqual(url_esperada, palestra.get_absolute_url())

    def test_get_absolute_url_sem_palestrante(self):
        palestra = models.Palestra.objects.get(pk=2)
        self.assertEqual("#", palestra.get_absolute_url())
