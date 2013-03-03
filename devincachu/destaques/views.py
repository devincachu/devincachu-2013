# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django.conf import settings
from django.template import response
from django.views.generic import base

from . import models


class IndexView(base.View):

    def obter_destaques(self):
        qs = models.Destaque.objects.select_related()
        return qs.order_by('-data')[:14]

    def get(self, request):
        contexto = {
            'destaques': self.obter_destaques(),
            'canonical_url': u"%s/" % settings.BASE_URL,
            'keywords': u", ".join([u"devincachu", "dev in cachu 2013",
                                    u"evento de informática",
                                    u"desenvolvimento de software",
                                    u"cachoeiro de itapemirim"]),
            'description': u"Dev in Cachu 2013 - principal evento sobre " +
                           u"desenvolvimento de software do " +
                           u"Espírito Santo",
        }
        return response.TemplateResponse(request, "index.html", contexto)
