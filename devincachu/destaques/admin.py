# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from django.contrib import admin

from . import forms, models


class DestaqueAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data',)
    list_filter = ('autor',)
    search_fields = ('titulo',)
    form = forms.DestaqueAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.autor = request.user

        obj.save()

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        return qs.filter(chamada__isnull=True)


class ChamadaAdmin(DestaqueAdmin):
    list_display = ('titulo', 'data', 'url_link')
    form = forms.ChamadaAdminForm

    def queryset(self, request):
        return admin.ModelAdmin.queryset(self, request)

try:
    admin.site.register(models.Destaque, DestaqueAdmin)
    admin.site.register(models.Chamada, ChamadaAdmin)
except admin.sites.AlreadyRegistered:
    pass
