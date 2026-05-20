from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Count, Avg, Q
from surveys.models import Feedback

class CourseAnalyticsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        qs = Feedback.objects.filter(course_id=pk, feedback_type="COURSE")
        
        if not qs.exists():
            return Response({"message": "No data available for this course."}, status=404)

        # 1. Base Aggregations (Sentiments & Ratings)
        sentiments = qs.aggregate(
            positive=Count('id', filter=Q(sentiment_label='POSITIVE')),
            neutral=Count('id', filter=Q(sentiment_label='NEUTRAL')),
            negative=Count('id', filter=Q(sentiment_label='NEGATIVE'))
        )
        ratings = qs.aggregate(
            avg_teaching=Avg('teaching_quality'),
            avg_content=Avg('course_content'),
            avg_engagement=Avg('engagement'),
            avg_satisfaction=Avg('overall_satisfaction'),
            average_sentiment_score=Avg('sentiment_score')
        )

        # 2. Recommendation & Anonymity Stats
        total_feedback = qs.count()
        total_recommendations = qs.exclude(would_recommend=None).count()
        recommended_count = qs.filter(would_recommend=True).count()
        anonymous_count = qs.filter(is_anonymous=True).count()

        # 3. Semester Trend (Groups data by semester)
        # Returns: [{'semester': 'SPRING', 'avg_score': 0.8, 'count': 12}, ...]
        semester_trend = qs.values('semester').annotate(
            count=Count('id'),
            avg_satisfaction=Avg('overall_satisfaction'),
            avg_sentiment=Avg('sentiment_score')
        ).order_by('semester')

        # 4. Recent Qualitative Highlights (Grabs latest 5)
        recent_comments = qs.order_by('-created_at').values(
            'created_at', 'positive_feedback', 'improvement_feedback', 'sentiment_label'
        )[:5]

        return Response({
            "total_feedback": total_feedback,
            "sentiment_distribution": sentiments,
            "average_ratings": {k: round(v, 2) for k, v in ratings.items() if v},
            "recommendation_rate": round((recommended_count / total_recommendations * 100), 1) if total_recommendations > 0 else 0,
            "anonymity_rate": round((anonymous_count / total_feedback * 100), 1),
            "semester_trends": list(semester_trend),
            "recent_comments": list(recent_comments)
        })


class InstructorAnalyticsView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        qs = Feedback.objects.filter(instructor_id=pk, feedback_type="INSTRUCTOR")
        
        if not qs.exists():
            return Response({"message": "No data available for this instructor."}, status=404)

        sentiments = qs.aggregate(
            positive=Count('id', filter=Q(sentiment_label='POSITIVE')),
            neutral=Count('id', filter=Q(sentiment_label='NEUTRAL')),
            negative=Count('id', filter=Q(sentiment_label='NEGATIVE'))
        )
        ratings = qs.aggregate(
            avg_teaching=Avg('teaching_quality'),
            avg_content=Avg('course_content'),
            avg_engagement=Avg('engagement'),
            avg_satisfaction=Avg('overall_satisfaction'),
            average_sentiment_score=Avg('sentiment_score')
        )

        total_feedback = qs.count()
        total_recommendations = qs.exclude(would_recommend=None).count()
        recommended_count = qs.filter(would_recommend=True).count()
        anonymous_count = qs.filter(is_anonymous=True).count()

        semester_trend = qs.values('semester').annotate(
            count=Count('id'),
            avg_satisfaction=Avg('overall_satisfaction'),
            avg_sentiment=Avg('sentiment_score')
        ).order_by('semester')

        recent_comments = qs.order_by('-created_at').values(
            'created_at', 'positive_feedback', 'improvement_feedback', 'sentiment_label'
        )[:5]

        return Response({
            "total_feedback": total_feedback,
            "sentiment_distribution": sentiments,
            "average_ratings": {k: round(v, 2) for k, v in ratings.items() if v},
            "recommendation_rate": round((recommended_count / total_recommendations * 100), 1) if total_recommendations > 0 else 0,
            "anonymity_rate": round((anonymous_count / total_feedback * 100), 1),
            "semester_trends": list(semester_trend),
            "recent_comments": list(recent_comments)
        })