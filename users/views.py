from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from core.permissions import IsAdminOrReadOnly, IsAdminUserAction

from .serializers import UserRegistrationSerializer, UserReadSerializer, UserUpdateSerializer

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            # Use our new serializer when they send a PUT/PATCH request
            return UserUpdateSerializer
            
        return UserReadSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        # Only admins can list all users or delete users
        elif self.action in ["list", "destroy"]:
            return [IsAdminUserAction()]
        # Authenticated users can view/update their own data
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        is_admin = user.is_superuser or getattr(user, 'user_type', None) == 'admin'

        # SECURITY: If they are NOT an admin, they can ONLY fetch/update their own row
        if not is_admin:
            queryset = queryset.filter(id=user.id)

        params = self.request.query_params
        if search := params.get("search"):
            queryset = queryset.filter(
                Q(email__icontains=search) | 
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search)
            )
        print("Final User queryset:", queryset)
        return queryset

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """Endpoint to get current logged in user details"""
        serializer = UserReadSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="deactivate")
    def deactivate(self, request):
        """Allows a user to soft-delete their own account"""
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated successfully."}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """Generates a password reset link for the given email"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"message": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "No user found with this email"}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        
        reset_link = f"/reset-password/{uid}/{token}/"
        
        return Response({
            "message": "Password reset link generated.",
            "link": reset_link
        }, status=200)


class ResetPasswordConfirmAPIView(APIView):
    """Verifies the token and uid, and sets the new password"""
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token): # Note: Changed to POST to receive the new password safely
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"message": "Invalid user ID"}, status=400)

        if not token_generator.check_token(user, token):
            return Response({"message": "Invalid or expired token"}, status=400)

        password = request.data.get("password")
        if not password:
            return Response({"message": "Password is required."}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=200)