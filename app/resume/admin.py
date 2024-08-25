from django.contrib import admin
from resume import models

# Register your models here.

admin.site.register(models.Skill)
admin.site.register(models.Education)
admin.site.register(models.Certificate)
admin.site.register(models.Experience)
