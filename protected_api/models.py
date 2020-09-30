
#from __future__ import unicode_literals
from django.db import models
from oauth2_provider.models import AbstractApplication
from django.utils.translation import ugettext_lazy as _
from protected_api.utils.common import APPLICATION_TYPE_USER, APPLICATION_TYPE_WEBAPP, APPLICATION_TYPE_ERP

class Gestore(models.Model):
    remote_db = models.CharField('Database di riferimento', max_length=250)
    name = models.CharField('Nome', max_length=250)

    def __str__(self):
        return self.name

APPLICATION_TYPES = (
        (APPLICATION_TYPE_USER, _('User')),
        (APPLICATION_TYPE_WEBAPP, _('Webapp')),
        (APPLICATION_TYPE_ERP, _('Erp')),
    )

class Application(AbstractApplication):
    gestore = models.ForeignKey(Gestore, on_delete=models.CASCADE)
    tipo = models.CharField(default=APPLICATION_TYPE_WEBAPP, choices=APPLICATION_TYPES, max_length=255)
    smartgrid_client_id = models.CharField(blank=True, max_length=255)#used if tipo is User

    def __str__(self):
        return self.name

