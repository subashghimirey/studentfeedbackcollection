from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Course, Instructor, Feedback
from .serializers import CourseSerializer, InstructorSerializer, FeedbackSerializer

from .services.sentiment_service import calculate_hybrid_sentiment


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # allow anyone to view courses
        return [IsAdminUser()]  # only admin can modify


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # allow anyone to view instructors
        return [IsAdminUser()] 


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user

        # 1. Base Queryset Filtering
        if user.is_staff or user.is_superuser or user.user_type == 'admin':
            # Admins see everything
            queryset = Feedback.objects.all()
        elif user.is_authenticated:
            # Regular users ONLY see feedback tied directly to their account
            queryset = Feedback.objects.filter(user=user)
        else:
            # Unauthenticated users see nothing
            return Feedback.objects.none()

        # 2. Existing URL filtering (Course, Instructor, Semester)
        course = self.request.query_params.get('course')
        instructor = self.request.query_params.get('instructor')
        semester = self.request.query_params.get('semester')

        if course:
            queryset = queryset.filter(course_id=course)
        if instructor:
            queryset = queryset.filter(instructor_id=instructor)
        if semester:
            queryset = queryset.filter(semester=semester)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        
        if str(self.request.data.get('is_anonymous', 'True')).lower() == 'true':
            user = None

         # Pass the entire validated dataset dictionary to our new smart service
        sentiment_data = calculate_hybrid_sentiment(serializer.validated_data)

        serializer.save(
            user=user,
            sentiment_score=sentiment_data["score"],
            sentiment_label=sentiment_data["label"]
        )