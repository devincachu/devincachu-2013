# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django import forms

from . import models


class PalestranteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Palestrante
        exclude = ('slug',)
        widgets = {
            'minicurriculo': forms.Textarea,
        }


class PalestraAdminForm(forms.ModelForm):
    class Meta:
        model = models.Palestra
        exclude = ('slug',)
        widgets = {
            'descricao': forms.Textarea,
        }
