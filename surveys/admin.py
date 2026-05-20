from django.contrib import admin
from . models import Course, Instructor, Feedback

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback_type', 'course', 'instructor', 'semester', 'created_at')
    list_filter = ('feedback_type', 'semester')
    search_fields = ('course__code', 'instructor__first_name', 'instructor__last_name')
    readonly_fields = ('sentiment_label', 'sentiment_score', 'created_at')
