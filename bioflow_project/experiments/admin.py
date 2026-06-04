from django.contrib import admin
from . import models
for name in dir(models):
    cls = getattr(models, name)
    try:
        if issubclass(cls, models.models.Model) and cls._meta.app_label == 'experiments':
            admin.site.register(cls)
    except TypeError:
        pass
