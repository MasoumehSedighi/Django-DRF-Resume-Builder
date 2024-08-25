"""
Url mappings for the resume app.
"""
from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from resume.api import views


router = DefaultRouter()
router.register('skills', views.SkillViewSet)
router.register('educations', views.EducationViewSet)


app_name = 'resume'

urlpatterns = [
    path('', include(router.urls)),
]
