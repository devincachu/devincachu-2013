# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.db import models as django_models

from .. import models


class ModelPalestranteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = [f.name for f in models.Palestrante._meta.fields]

    def test_model_palestrante_deve_ter_nome(self):
        self.assertIn('nome', self.field_names)

    def test_campo_nome_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_nome_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertFalse(field.blank)

    def test_campo_nome_deve_ter_no_maximo_100_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'nome'][0]
        self.assertEquals(100, field.max_length)

    def test_model_palestrante_deve_ter_slug(self):
        self.assertIn('slug', self.field_names)

    def test_campo_slug_deve_ser_SlugField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'slug'][0]
        self.assertIsInstance(field, django_models.SlugField)

    def test_campo_slug_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'slug'][0]
        self.assertFalse(field.blank)

    def test_campo_slug_deve_ter_no_maximo_100_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'slug'][0]
        self.assertEquals(100, field.max_length)

    def test_campo_slug_deve_ser_unico(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'slug'][0]
        self.assertTrue(field.unique)

    def test_model_palestrante_deve_ter_blog(self):
        self.assertIn('blog', self.field_names)

    def test_campo_blog_deve_ser_URLField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertIsInstance(field, django_models.URLField)

    def test_campo_blog_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertTrue(field.blank)

    def test_campo_blog_deve_ter_verify_false(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        validator = field.validators[1]
        self.assertFalse(validator.verify_exists)

    def test_campo_blog_deve_ter_no_maximo_255_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'blog'][0]
        self.assertEquals(255, field.max_length)

    def test_model_palestrante_deve_ter_campo_para_perfil_no_twitter(self):
        self.assertIn('twitter', self.field_names)

    def test_campo_twitter_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_twitter_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertTrue(field.blank)

    def test_campo_twitter_deve_ter_no_maximo_50_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'twitter'][0]
        self.assertEquals(50, field.max_length)

    def test_model_palestrante_deve_ter_campo_para_minicurriculo(self):
        self.assertIn('minicurriculo', self.field_names)

    def test_campo_minicurriculo_deve_ser_CharField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_minicurriculo_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertFalse(field.blank)

    def test_campo_minicurriculo_deve_ter_no_maximo_1000_caracteres(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'minicurriculo'][0]
        self.assertEquals(1000, field.max_length)

    def test_palestrante_deve_ter_foto(self):
        self.assertIn('foto', self.field_names)

    def test_campo_foto_deve_ser_do_tipo_ImageField(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertIsInstance(field, django_models.ImageField)

    def test_campo_foto_deve_enviar_fotos_para_diretorio_palestrantes(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertEquals("palestrantes", field.upload_to)

    def test_campo_foto_nao_deve_aceitar_blank(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'foto'][0]
        self.assertFalse(field.blank)

    def test_palestrante_deve_ter_flag_de_listagem_na_pagina(self):
        self.assertIn('listagem', self.field_names)

    def test_flag_de_listagem_deve_ser_do_tipo_boolean(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'listagem'][0]
        self.assertIsInstance(field, django_models.BooleanField)

    def test_flag_de_listagem_deve_ter_verbose_name_bonitinho(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'listagem'][0]
        self.assertEquals(u"Exibir na página de palestrantes?", field.verbose_name)

    def test_flag_de_listagem_deve_vir_desmarcado_por_padrao(self):
        field = [f for f in models.Palestrante._meta.fields if f.name == 'listagem'][0]
        self.assertEquals(False, field.default)

    def test_repr_deve_conter_nome_do_palestrante(self):
        esperado = '<Palestrante: "Francisco Souza">'
        palestrante = models.Palestrante(nome="Francisco Souza")
        self.assertEquals(esperado, repr(palestrante))

    def test_unicode_deve_retornar_nome_do_palestrante(self):
        palestrante = models.Palestrante(nome="Francisco Souza")
        self.assertEquals("Francisco Souza", unicode(palestrante))

    def test_str_deve_retornar_nome_do_palestrante(self):
        palestrante = models.Palestrante(nome="Francisco Souza")
        self.assertEquals("Francisco Souza", str(palestrante))
