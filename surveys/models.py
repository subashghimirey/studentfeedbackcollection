from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

User = get_user_model()

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

SEMESTER_CHOICES = [
    ('SPRING', 'Spring'),
    ('SUMMER', 'Summer'),
    ('FALL', 'Fall'),
    ('WINTER', 'Winter')
]

SENTIMENT_CHOICES = [
    ("POSITIVE", "Positive"),
    ("NEUTRAL", "Neutral"),
    ("NEGATIVE", "Negative"),
]

FEEDBACK_TYPE_CHOICES = [
    ("COURSE", "Course Feedback"),
    ("INSTRUCTOR", "Instructor Feedback"),
]


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code


class Instructor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    # User
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Context
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # Instructor is optional but conditionally required
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)

    # Control
    is_anonymous = models.BooleanField(default=True)

    # Ratings
    teaching_quality = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    course_content = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    engagement = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_satisfaction = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # Text (for NLP)
    positive_feedback = models.TextField()
    improvement_feedback = models.TextField()

    # Optional
    would_recommend = models.BooleanField(null=True, blank=True)

    # Sentiment (auto-generated)
    sentiment_label = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        blank=True,
        null=True
    )
    sentiment_score = models.FloatField(blank=True, null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Enforce logical consistency between feedback_type and instructor
        """
        if self.feedback_type == "INSTRUCTOR" and not self.instructor:
            raise ValidationError("Instructor is required for instructor feedback.")

        if self.feedback_type == "COURSE" and self.instructor:
            raise ValidationError("Instructor should not be provided for course feedback.")

    def __str__(self):
        return f"{self.feedback_type} - {self.course.code} - {self.created_at.date()}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['instructor']),
            models.Index(fields=['semester']),
            models.Index(fields=['feedback_type']),
        ]