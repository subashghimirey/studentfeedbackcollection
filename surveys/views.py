from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import Course, Instructor, Feedback
from .serializers import CourseSerializer, InstructorSerializer, FeedbackSerializer


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
        return [IsAdminUser()]  # restrict write access


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        user = self.request.user

        # Only admins can see all feedback
        if user.is_staff:
            queryset = Feedback.objects.all()
        else:
            queryset = Feedback.objects.none()

        # filtering 
        course = self.request.query_params.get('course')
        instructor = self.request.query_params.get('instructor')
        semester = self.request.query_params.get('semester')

        if course:
            queryset = queryset.filter(course_id=course)
        if instructor:
            queryset = queryset.filter(instructor_id=instructor)
        if semester:
            queryset = queryset.filter(semester=semester)
        
        print(f"FeedbackViewSet: user={user}, course={course}, instructor={instructor}, semester={semester}, count={queryset.count()}")

        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # allow anonymous submission
        
        return [IsAuthenticated()]  # viewing requires login

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_authenticated and not self.request.data.get('is_anonymous', True):
            serializer.save(user=user)
        else:
            serializer.save(user=None)