# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django.db import models as django_models

from .. import models


class ParticipanteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.field_names = models.Participante._meta.get_all_field_names()

    def test_deve_ter_campo_com_o_nome_do_participante(self):
        self.assertIn("nome", self.field_names)

    def test_nome_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("nome")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_nome_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("nome")[0]
        self.assertEqual(100, field.max_length)

    def test_deve_ter_campo_nome_no_cracha(self):
        self.assertIn("nome_cracha", self.field_names)

    def test_nome_no_cracha_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_nome_no_cracha_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertEqual(100, field.max_length)

    def test_nome_no_cracha_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_nome_no_cracha_deve_ter_verbose_name_com_acento(self):
        field = models.Participante._meta.get_field_by_name("nome_cracha")[0]
        self.assertEqual(u"Nome no crachá", field.verbose_name)

    def test_deve_ter_campo_sexo(self):
        self.assertIn("sexo", self.field_names)

    def test_campo_sexo_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_sexo_deve_ter_no_maximo_1_caracter(self):
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertEqual(1, field.max_length)

    def test_campo_sexo_deve_ter_m_ou_f(self):
        esperado = (
            (u"M", u"Masculino"),
            (u"F", u"Feminino"),
        )
        field = models.Participante._meta.get_field_by_name("sexo")[0]
        self.assertEqual(esperado, field.choices)

    def test_deve_ter_campo_email(self):
        self.assertIn("email", self.field_names)

    def test_email_deve_ser_do_tipo_EmailField(self):
        field = models.Participante._meta.get_field_by_name("email")[0]
        self.assertIsInstance(field, django_models.EmailField)

    def test_email_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("email")[0]
        self.assertEqual(100, field.max_length)

    def test_email_e_status_devem_ser_unique_juntos(self):
        self.assertEqual((u'email', u'status'),
                         models.Participante._meta.unique_together[0])

    def test_deve_ter_campo_status(self):
        self.assertIn("status", self.field_names)

    def test_campo_status_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_campo_status_deve_ter_no_maximo_20_caracteres(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEqual(20, field.max_length)

    def test_campo_stauts_deve_ser_AGUARDANDO_por_padrao(self):
        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEqual(u"AGUARDANDO", field.default)

    def test_campo_status_deve_ter_choices_adequados(self):
        esperado = (
            (u'AGUARDANDO', u'Aguardando pagamento'),
            (u'CONFIRMADO', u'Confirmado'),
            (u'CANCELADO', u'Cancelado'),
            (u'CORTESIA', u'Cortesia'),
            (u'PALESTRANTE', u'Palestrante'),
            (u'ORGANIZACAO', u'Organização'),
            (u'CARAVANA', u'Caravana'),
        )

        field = models.Participante._meta.get_field_by_name("status")[0]
        self.assertEqual(esperado, field.choices)

    def test_deve_ter_campo_para_tamanho_de_camiseta(self):
        self.assertIn("tamanho_camiseta", self.field_names)

    def test_tamanho_de_camiseta_deve_ser_CharField(self):
        field = models.Participante._meta.get_field_by_name(
            "tamanho_camiseta")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_tamanho_de_camiseta_deve_ter_no_maximo_2_caracteres(self):
        field = models.Participante._meta.get_field_by_name(
            "tamanho_camiseta")[0]
        self.assertEqual(2, field.max_length)

    def test_tamanho_de_camiseta_deve_ter_verbose_name_descritivo(self):
        field = models.Participante._meta.get_field_by_name(
            "tamanho_camiseta")[0]
        self.assertEqual(u"Tamanho da camiseta", field.verbose_name)

    def test_tamanho_de_camiseta_deve_ter_options_limitadas(self):
        esperado = (
            (u'P', u'P (53cm x 71cm)'),
            (u'M', u'M (56cm x 74cm)'),
            (u'G', u'G (58cm x 76cm)'),
            (u'GG', u'GG (62cm x 80cm)'),
        )
        field = models.Participante._meta.get_field_by_name(
            "tamanho_camiseta")[0]
        self.assertEqual(esperado, field.choices)

    def test_deve_ter_instituicao_de_ensino(self):
        self.assertIn("instituicao_ensino", self.field_names)

    def test_instituicao_de_ensino_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name(
            "instituicao_ensino")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_instituicao_de_ensino_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name(
            "instituicao_ensino")[0]
        self.assertEqual(100, field.max_length)

    def test_instituicao_de_ensino_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name(
            "instituicao_ensino")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_instituicao_de_ensino_verbose_name_deve_citar_estudante(self):
        field = models.Participante._meta.get_field_by_name(
            "instituicao_ensino")[0]
        self.assertEqual(u"Instituição de ensino (estudantes)",
                         field.verbose_name)

    def test_deve_ter_empresa(self):
        self.assertIn("empresa", self.field_names)

    def test_empresa_deve_ser_do_tipo_CharField(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_empresa_deve_ter_no_maximo_100_caracteres(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertEqual(100, field.max_length)

    def test_empresa_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_empresa_deve_ter_verbose_name_empresa_onde_trabalha(self):
        field = models.Participante._meta.get_field_by_name("empresa")[0]
        self.assertEqual(u"Empresa onde trabalha", field.verbose_name)

    def test_deve_ter_cidade_estado(self):
        self.assertIn("cidade", self.field_names)

    def test_cidade_estado_deve_ser_CharField(self):
        field = models.Participante._meta.get_field_by_name("cidade")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_cidade_estado_deve_ter_no_maximo_255_caracteres(self):
        field = models.Participante._meta.get_field_by_name("cidade")[0]
        self.assertEqual(255, field.max_length)

    def test_cidade_estado_deve_ter_verbose_name_com_barra(self):
        field = models.Participante._meta.get_field_by_name("cidade")[0]
        self.assertEqual(u"Cidade/Estado", field.verbose_name)

    def test_deve_ter_field_presente(self):
        self.assertIn("presente", self.field_names)

    def test_presente_deve_ser_boolean_field(self):
        field = models.Participante._meta.get_field_by_name("presente")[0]
        self.assertIsInstance(field, django_models.BooleanField)

    def test_presente_deve_ser_False_por_padrao(self):
        field = models.Participante._meta.get_field_by_name("presente")[0]
        self.assertEqual(False, field.default)

    def test_deve_ter_campo_observacao(self):
        self.assertIn("observacao", self.field_names)

    def test_observacao_deve_ter_char_field(self):
        field = models.Participante._meta.get_field_by_name("observacao")[0]
        self.assertIsInstance(field, django_models.CharField)

    def test_observacao_deve_ter_no_maximo_1000_chars(self):
        field = models.Participante._meta.get_field_by_name("observacao")[0]
        self.assertEqual(1000, field.max_length)

    def test_observacao_nao_deve_ser_obrigatorio(self):
        field = models.Participante._meta.get_field_by_name("observacao")[0]
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_observacao_deve_ter_verbose_name(self):
        field = models.Participante._meta.get_field_by_name("observacao")[0]
        self.assertEqual(u"Observação", field.verbose_name)

    def test__repr__deve_ter_nome(self):
        participante = models.Participante(nome=u"Francisco Souza")
        self.assertEqual(u"<Participante: Francisco Souza>",
                         repr(participante))

    def test__unicode__deve_ser_o_nome(self):
        participante = models.Participante(nome=u"Francisco Souza")
        self.assertEqual(u"Francisco Souza", unicode(participante))
