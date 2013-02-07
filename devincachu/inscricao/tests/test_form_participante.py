# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django import forms as django_forms

from .. import models, forms


class ParticipanteFormTestCase(unittest.TestCase):

    def test_deve_ser_um_ModelForm(self):
        assert issubclass(forms.ParticipanteForm, django_forms.ModelForm)

    def test_model_deve_ser_Participante(self):
        self.assertEqual(models.Participante, forms.ParticipanteForm.Meta.model)

    def test_nao_deve_trazer_campo_confirmado_do_model(self):
        self.assertIn("status", forms.ParticipanteForm.Meta.exclude)

    def test_deve_ter_estilo_para_campos_obrigatorios(self):
        self.assertEqual("obrigatorio", forms.ParticipanteForm.required_css_class)

    def test_deve_ter_estilo_para_campos_com_erro(self):
        self.assertEqual("error", forms.ParticipanteForm.error_css_class)
