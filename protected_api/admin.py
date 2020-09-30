from django.contrib import admin

# Register your models here.

from .models import Application, Gestore

admin.site.register(Gestore)
#admin.site.register(Application)