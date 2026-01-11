from django.urls import path
from . import views

urlpatterns = [
    path('session/save/', views.SaveGameSessionView.as_view()),
    path('session/load/', views.LoadLastSessionView.as_view()),
    path('leaderboard/', views.LeaderboardView.as_view()),
    path('achievements/', views.UserAchievementsView.as_view()),
    path('friends/add/', views.AddFriendView.as_view()),
    path('friends/', views.FriendsListView.as_view()),
]