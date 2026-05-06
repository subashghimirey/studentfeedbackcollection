from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, InstructorViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'instructors', InstructorViewSet, basename='instructor')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
]