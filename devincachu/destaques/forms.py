# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django import forms

from . import models


class DestaqueAdminForm(forms.ModelForm):
    class Meta:
        model = models.Destaque
        exclude = ('autor', 'data')
        widgets = {
            'conteudo': forms.Textarea,
        }
