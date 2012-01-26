# -*- coding: utf-8 -*-
from django.db import models


class Palestrante(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    minicurriculo = models.CharField(max_length=1000)
    blog = models.URLField(verify_exists=False, max_length=255, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    foto = models.ImageField(upload_to=u"palestrantes")

    def __repr__(self):
        return '<Palestrante: "%s">' % self.nome

    def __unicode__(self):
        return self.nome


class Palestra(models.Model):
    titulo = models.CharField(max_length=150, verbose_name=u"Título")
    slug = models.SlugField(max_length=150, unique=True)
    descricao = models.CharField(max_length=1000, verbose_name=u"Descrição")
    inicio = models.TimeField(verbose_name=u"Horário de início")
    termino = models.TimeField(verbose_name=u"Horário de término")
    palestrantes = models.ManyToManyField(Palestrante, blank=True)

    def nomes_palestrantes(self, palestrantes=None):
        palestrantes = palestrantes or self.palestrantes.order_by("nome")
        nomes = [p.nome for p in palestrantes]
        nomes = ", ".join(nomes)

        if "," in nomes:
            indice = nomes.rfind(",")
            nomes = "%s e %s" % (nomes[:indice], nomes[indice + 2:])

        return nomes

    def __repr__(self):
        return "<Palestra: %s>" % self.titulo

    def __unicode__(self):
        return self.titulo

    def get_absolute_url_and_link_title(self):
        palestrantes = self.palestrantes.order_by("nome")

        prefixo = "/".join([p.slug for p in palestrantes])

        if prefixo:
            url = "/programacao/%s/%s/" % (prefixo, self.slug)
            trecho = "dos palestrantes" if "/" in prefixo else "do palestrante"
            titulo = u"Veja mais informações da palestra %s e %s %s" % (self.titulo, trecho, self.nomes_palestrantes(palestrantes))
            return {'url': url, 'title': titulo}

        return {'url': "#", 'title': self.descricao}
