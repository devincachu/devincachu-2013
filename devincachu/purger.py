# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import roan

from django.contrib.flatpages import models

from palestras import models as pmodels


def connect():
    flatpages = models.FlatPage.objects.all()
    for f in flatpages:
        roan.purge(f.url).on_save(models.FlatPage)

    palestras = pmodels.Palestra.objects.all()
    for p in palestras:
        roan.purge(p.get_absolute_url()).on_save(pmodels.Palestra)
        roan.purge(p.get_absolute_url()).on_delete(pmodels.Palestra)
        roan.purge(p.get_absolute_url()).on_save(pmodels.Palestrante)
        roan.purge(p.get_absolute_url()).on_delete(pmodels.Palestrante)
