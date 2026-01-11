from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь существует'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        UserProfile.objects.create(user=user)
        return Response({'message': 'Пользователь создан'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from rest_framework_simplejwt.views import TokenObtainPairView
        from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class ProfileView(APIView):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class ProfileUpdateView(APIView):
    def patch(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)