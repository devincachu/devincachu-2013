# -*- coding: utf-8 -*-

# Copyright 2013 Dev in Cachu authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import roan

from django.contrib.auth import models as auth_models
from django.db import models


class Destaque(models.Model):
    titulo = models.CharField(max_length=60)
    conteudo = models.CharField(max_length=500)
    autor = models.ForeignKey(auth_models.User)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __repr__(self):
        return "<Destaque: %s>" % self.titulo

    def __unicode__(self):
        return self.titulo


roan.purge("/").on_save(Destaque)
roan.purge("/").on_delete(Destaque)
