# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django import forms

from . import models


class ParticipanteForm(forms.ModelForm):
    error_css_class = u"error"
    required_css_class = u"obrigatorio"

    class Meta:
        model = models.Participante
        exclude = ("status", "presente", "observacao")


class ValidacaoCertificado(forms.Form):
    codigo = forms.CharField(max_length=30)
    error_css_class = u"error"

    def obter_certificado(self):
        if self.is_valid():
            try:
                qs = models.Certificado.objects.select_related("participante")
                return qs.get(codigo=self.cleaned_data["codigo"])
            except models.Certificado.DoesNotExist:
                return None


class BuscarCertificado(forms.Form):
    email = forms.EmailField(max_length=100)
    error_css_class = u"error"

    def obter_certificado(self):
        if self.is_valid():
            try:
                qs = models.Certificado.objects.select_related("participante")
                return qs.get(participante__email=self.cleaned_data["email"])
            except models.Certificado.DoesNotExist:
                return None
