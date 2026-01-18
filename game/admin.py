from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Achievement, UserAchievement, GameSession, LeaderboardEntry, Friendship

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')
    list_filter = ('achievement',)

@admin.register(GameSession)
class GameSessionAdmin(ImportExportModelAdmin):
    list_display = ('user', 'score', 'difficulty', 'time_played', 'is_completed', 'created_at')
    list_filter = ('difficulty', 'is_completed')
    search_fields = ('user__username',)

@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'rank', 'date_achieved')
    ordering = ('-score',)

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('from_user__username', 'to_user__username')
    ordering = ('-created_at',)