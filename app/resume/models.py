from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='skills',
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.title}'
