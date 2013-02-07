# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django import forms as django_forms

from .. import forms, models


class PalestranteAdminFormTestCase(unittest.TestCase):

    def test_PalestranteAdminForm_deve_ser_um_ModelForm(self):
        assert issubclass(forms.PalestranteAdminForm, django_forms.ModelForm)

    def test_PalestranteAdminForm_deve_ter_model_Palestrante_no_meta(self):
        self.assertEqual(models.Palestrante, forms.PalestranteAdminForm.Meta.model)

    def test_PalestranteAdminForm_deve_excluir_campo_slug(self):
        self.assertIn('slug', forms.PalestranteAdminForm.Meta.exclude)

    def test_deve_utilizar_widget_de_textarea_para_minicurriculo(self):
        self.assertEqual(django_forms.Textarea, forms.PalestranteAdminForm.Meta.widgets['minicurriculo'])


class PalestraAdminFormTestCase(unittest.TestCase):

    def test_PalestraAdminForm_deve_ser_um_ModelForm(self):
        assert issubclass(forms.PalestraAdminForm, django_forms.ModelForm)

    def test_PalestraAdminForm_deve_ter_model_Palestra_no_meta(self):
        self.assertEqual(models.Palestra, forms.PalestraAdminForm.Meta.model)

    def test_PalestraAdminForm_deve_excluir_campo_slug(self):
        self.assertIn('slug', forms.PalestraAdminForm.Meta.exclude)

    def test_PalestraAdminForm_deve_utilizar_widget_de_textarea_para_descricao_de_palestra(self):
        self.assertEqual(django_forms.Textarea, forms.PalestraAdminForm.Meta.widgets['descricao'])
