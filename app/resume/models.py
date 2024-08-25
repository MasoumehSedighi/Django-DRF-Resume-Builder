from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    """
    An abstract base model that provides
    common timestamp fields for other models.
    """

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Skill(BaseModel):
    """
    A model representing a user's skill.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='skills',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user} - {self.title}'


class Education(BaseModel):
    """
    A model representing a user's educational background.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='educations',
        on_delete=models.CASCADE
    )
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('start_date',)

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("start date must be before the end date")


class Certificate(BaseModel):
    """
    A model representing a user's certificates.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='certificates',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()

    class Meta:
        ordering = ('-issue_date',)

    def __str__(self):
        return f'{self.user} - {self.title}'
