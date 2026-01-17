from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import GameSession, LeaderboardEntry, UserAchievement, Friendship
from .serializers import GameSessionSerializer, LeaderboardSerializer, UserAchievementSerializer, FriendSerializer
from django.db.models import Max
from django.contrib.auth.models import User

class SaveGameSessionView(APIView):
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = GameSessionSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save()
            # Обновляем лидерборд
            best_score = GameSession.objects.filter(user=request.user, is_completed=True).aggregate(Max('score'))['score__max'] or 0
            entry, created = LeaderboardEntry.objects.update_or_create(
                user=request.user,
                defaults={'score': best_score}
            )
            # Здесь можно добавить логику достижений
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoadLastSessionView(APIView):
    def get(self, request):
        session = GameSession.objects.filter(user=request.user).order_by('-created_at').first()
        if session:
            return Response(GameSessionSerializer(session).data)
        return Response({'message': 'Нет сохранений'})

class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        entries = LeaderboardEntry.objects.all().order_by('-score')[:50]
        for i, entry in enumerate(entries):
            entry.rank = i + 1
            entry.save()
        serializer = LeaderboardSerializer(entries, many=True)
        return Response(serializer.data)

class UserAchievementsView(APIView):
    def get(self, request):
        achievements = UserAchievement.objects.filter(user=request.user)
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

class AddFriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Укажите username'}, status=status.HTTP_400_BAD_REQUEST)
        
        if username == request.user.username:
            return Response({'error': 'Нельзя добавить себя в друзья'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            Friendship.objects.get_or_create(from_user=request.user, to_user=friend)
            Friendship.objects.get_or_create(from_user=friend, to_user=request.user)  # Симметрично
            return Response({'message': 'Друг добавлен'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'error': 'Вы уже друзья'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FriendsListView(APIView):
    def get(self, request):
        friends = Friendship.objects.filter(from_user=request.user, accepted=True)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)