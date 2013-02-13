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

try:
    admin.site.register(models.Destaque, DestaqueAdmin)
except admin.sites.AlreadyRegistered:
    pass
