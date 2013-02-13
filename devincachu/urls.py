# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.views.decorators import csrf
from django.views.generic import base

from django.contrib import admin
admin.autodiscover()

from devincachu.destaques import views as dviews
from devincachu.inscricao import views as iviews
from devincachu.palestras import views as pviews

from purger import connect
connect()

p = patterns
urlpatterns = p("",
                url(r"^admin/", include(admin.site.urls)),
                url(r"^palestrantes/$",
                    pviews.PalestrantesView.as_view(),
                    name="palestrantes"),
                url(r"^programacao/$",
                    pviews.ProgramacaoView.as_view(),
                    name="programacao"),
                url(r"^programacao/(?P<palestrantes>.*)/(?P<slug>[\w-]+)/$",
                    pviews.PalestraView.as_view(),
                    name="palestra"),
                url(r"^inscricao/$",
                    iviews.Inscricao.as_view(),
                    name="inscricao"),
                url(r"^notificacao/$",
                    csrf.csrf_exempt(iviews.Notificacao.as_view()),
                    name="notificacao"),
                url(r"^certificado/validar/$",
                    iviews.ValidacaoCertificado.as_view(),
                    name="validacao_certificado"),
                url(r"^certificado/$",
                    iviews.BuscarCertificado.as_view(),
                    name="busca_certificado"),
                url(r"^certificado/(?P<slug>[0-9a-f]+)/$",
                    iviews.Certificado.as_view(),
                    name="certificado"),
                url(r"^quando-e-onde/$",
                    base.TemplateView.as_view(
                        template_name="quando-e-onde.html",
                    ),
                    name="quando-e-onde"),
                url(r"^$", dviews.IndexView.as_view(), name="index"),
                )

if settings.DEBUG:
    urlpatterns += patterns("",
                            url(r"^media/(?P<path>.*)$",
                            "django.views.static.serve",
                            {"document_root": settings.MEDIA_ROOT}),
                            )
