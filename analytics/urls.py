from django.urls import path
from .views import CourseAnalyticsView, InstructorAnalyticsView

urlpatterns = [
    path('courses/<int:pk>/', CourseAnalyticsView.as_view(), name='course-analytics'),
    path('instructors/<int:pk>/', InstructorAnalyticsView.as_view(), name='instructor-analytics'),
]