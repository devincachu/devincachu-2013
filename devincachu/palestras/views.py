# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django.conf import settings
from django.views.generic import detail, list

from . import models


class PalestrantesView(list.ListView):
    context_object_name = u"palestrantes"
    model = models.Palestrante
    template_name = u"palestrantes.html"
    queryset = models.Palestrante.objects.filter(listagem=True)
    queryset = queryset.order_by(u"nome")

    def get_context_data(self, **kwargs):
        context = super(PalestrantesView, self).get_context_data(**kwargs)
        context.update({
            u"keywords": u"dev in cachu, palestrantes, %s" % u", "
                         .join([p.nome for p in
                                context["palestrantes"]]),
            u"description": u"Palestrantes do Dev in Cachu 2013",
            u"canonical_url": u"%s/palestrantes/" % settings.BASE_URL
        })

        return context


class ProgramacaoView(list.ListView):
    context_object_name = u"palestras"
    model = models.Palestra
    template_name = u"programacao.html"
    queryset = models.Palestra.objects.all().order_by(u"inicio")

    def get_context_data(self, **kwargs):
        context = super(ProgramacaoView, self).get_context_data(**kwargs)
        keywords = [u"devincachu", u"dev in cachu 2013", u"palestras",
                    u"programação", u"desenvolvimento de software"]
        context.update({
            u"keywords": u", ".join(keywords),
            u"description": u"Grade de programação do Dev in Cachu 2013",
            u"canonical_url": u"%s/programacao/" % settings.BASE_URL,
        })
        return context


class PalestraView(detail.DetailView):
    context_object_name = u"palestra"
    model = models.Palestra
    template_name = u"palestra.html"

    def get_queryset(self):
        slugs_palestrantes = self.kwargs[u"palestrantes"].split(u"/")
        qs = models.Palestra.objects.filter(
            slug=self.kwargs[u"slug"],
            palestrantes__slug__in=slugs_palestrantes,
        )
        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super(PalestraView, self).get_context_data(**kwargs)
        keywords = [u"dev in cachu 2012", u"palestra",
                    context[u"palestra"].titulo,
                    context[u"palestra"].nomes_palestrantes()
                    .replace(u" e ", u", ")]
        context.update({
            u"keywords": u", ".join(keywords),
            u"description": context[u"palestra"].descricao,
            u"canonical_url": u"%s/programacao/%s/%s/" %
            (settings.BASE_URL, self.kwargs[u"palestrantes"],
             self.kwargs[u"slug"]),
        })
        return context
