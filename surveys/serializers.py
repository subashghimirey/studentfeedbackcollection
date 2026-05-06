from rest_framework import serializers
from .models import Course, Instructor, Feedback


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user', 'sentiment_label', 'sentiment_score', 'created_at']

    def validate(self, data):
        feedback_type = data.get("feedback_type")
        instructor = data.get("instructor")

        if feedback_type == "INSTRUCTOR" and not instructor:
            raise serializers.ValidationError({
                "instructor": "Instructor is required for instructor feedback."
            })

        if feedback_type == "COURSE" and instructor:
            raise serializers.ValidationError({
                "instructor": "Do not provide instructor for course feedback."
            })

        return data

    def create(self, validated_data):
        # Handle anonymity safely
        if validated_data.get('is_anonymous', True):
            validated_data['user'] = None

        return super().create(validated_data)