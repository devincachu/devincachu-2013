# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from django import forms as django_forms

from .. import forms, models


class DestaqueAdminFormTestCase(unittest.TestCase):

    def test_DestaqueAdminForm_deve_ser_um_ModelForm(self):
        assert issubclass(forms.DestaqueAdminForm, django_forms.ModelForm)

    def test_DestaqueAdminForm_deve_ter_model_Destaque_no_meta(self):
        self.assertEquals(models.Destaque, forms.DestaqueAdminForm.Meta.model)

    def test_DestaqueAdminForm_deve_excluir_campo_data(self):
        self.assertIn('data', forms.DestaqueAdminForm.Meta.exclude)

    def test_DestaqueAdminForm_deve_excluir_campo_autor(self):
        self.assertIn('autor', forms.DestaqueAdminForm.Meta.exclude)

    def test_deve_utilizar_o_widget_de_text_area_para_conteudo(self):
        self.assertEquals(django_forms.Textarea,
                          forms.DestaqueAdminForm.Meta.widgets['conteudo'])


class ChamadaAdminFormTestCase(unittest.TestCase):

    def test_ChamadaAdminForm_deve_ser_um_ModelForm(self):
        assert issubclass(forms.ChamadaAdminForm, django_forms.ModelForm)

    def test_Meta_do_ChamadaAdminForm_herda_do_Meta_do_parent(self):
        assert issubclass(forms.ChamadaAdminForm.Meta,
                          forms.DestaqueAdminForm.Meta)

    def test_ChamadaAdminForm_deve_ter_model_chamada_no_meta(self):
        self.assertEquals(models.Chamada, forms.ChamadaAdminForm.Meta.model)
