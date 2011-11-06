from django.conf.urls.defaults import include, patterns, url
from django.views.generic import list

from django.contrib import admin
admin.autodiscover()

from destaques import models


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', list.ListView.as_view(template_name='index.html', queryset=models.Destaque.objects.select_related().order_by('-data')[:10], context_object_name='destaques'), name='index'),
)
