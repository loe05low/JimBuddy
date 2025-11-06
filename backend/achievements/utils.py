# coding: utf-8
from .models import Achievement, UserAchievement
from social.models import Follow
from notifications.models import Notification


def check_and_unlock_achievements(user_profile):
    """
    Check all achievements and unlock any that the user qualifies for
    Returns list of newly unlocked achievements
    """
    newly_unlocked = []

    # Get all achievements
    all_achievements = Achievement.objects.all()

    for achievement in all_achievements:
        # Check if user already has this achievement
        user_achievement, created = UserAchievement.objects.get_or_create(
            user=user_profile,
            achievement=achievement,
            defaults={'progress': 0}
        )

        # Skip if already unlocked
        if user_achievement.is_unlocked:
            continue

        # Calculate current progress based on achievement key
        current_progress = calculate_progress(user_profile, achievement.key)

        # Update progress
        old_progress = user_achievement.progress
        user_achievement.progress = current_progress
        user_achievement.save()

        # Check if newly unlocked
        if user_achievement.is_unlocked and old_progress < achievement.required_count:
            newly_unlocked.append(user_achievement)

            # Create notification
            Notification.objects.create(
                user=user_profile,
                tip='achievement_unlocked',
                titlu=f'Achievement Unlocked! {achievement.icon}',
                mesaj=f'You unlocked: {achievement.name}',
                link='/achievements'
            )

    return newly_unlocked


def calculate_progress(user_profile, achievement_key):
    """
    Calculate user's progress for a specific achievement
    """
    # Workout achievements
    if achievement_key in ['first_workout', 'workout_10', 'workout_50', 'workout_100', 'workout_500']:
        return user_profile.nr_antrenamente

    # Social achievements
    elif achievement_key == 'first_rating':
        from ratings.models import Rating
        return Rating.objects.filter(rater=user_profile).count()

    elif achievement_key in ['first_follow', 'follow_10', 'follow_50']:
        return Follow.objects.filter(follower=user_profile).count()

    elif achievement_key in ['popular', 'popular_50', 'popular_100']:
        return Follow.objects.filter(following=user_profile).count()

    # Exploration achievements
    elif achievement_key in ['gym_explorer', 'gym_nomad']:
        return user_profile.sesiuni.values('sala').distinct().count()

    elif achievement_key == 'social_butterfly':
        followers = Follow.objects.filter(following=user_profile).count()
        following = Follow.objects.filter(follower=user_profile).count()
        return min(followers, following)

    else:
        return 0


def create_default_achievements():
    """
    Create default achievements in the database
    Call this from Django management command or shell
    """
    achievements_data = [
        ('first_workout', 'First Workout', 'Complete your first workout session', 'workout', 1, 10, 'common', '\U0001F4AA'),
        ('workout_10', 'Workout Warrior', 'Complete 10 workout sessions', 'workout', 10, 25, 'common', '\U0001F525'),
        ('workout_50', 'Fitness Fanatic', 'Complete 50 workout sessions', 'workout', 50, 50, 'rare', '\U0001F4AF'),
        ('workout_100', 'Century Club', 'Complete 100 workout sessions', 'workout', 100, 100, 'epic', '\U0001F3C6'),
        ('workout_500', 'Legendary Athlete', 'Complete 500 workout sessions', 'workout', 500, 500, 'legendary', '\U0001F451'),
        ('first_rating', 'First Impression', 'Rate your first gym buddy', 'social', 1, 10, 'common', '\u2B50'),
        ('first_follow', 'Making Friends', 'Follow your first user', 'social', 1, 10, 'common', '\U0001F465'),
        ('follow_10', 'Networker', 'Follow 10 users', 'social', 10, 20, 'common', '\U0001F91D'),
        ('follow_50', 'Connector', 'Follow 50 users', 'social', 50, 50, 'rare', '\U0001F310'),
        ('popular', 'Popular', 'Get 10 followers', 'social', 10, 30, 'common', '\U0001F31F'),
        ('popular_50', 'Influencer', 'Get 50 followers', 'social', 50, 75, 'rare', '\U0001F4C8'),
        ('popular_100', 'Celebrity', 'Get 100 followers', 'social', 100, 150, 'epic', '\U0001F48E'),
        ('social_butterfly', 'Social Butterfly', 'Have 20+ followers AND follow 20+ users', 'social', 20, 100, 'epic', '\U0001F98B'),
        ('gym_explorer', 'Gym Explorer', 'Visit 5 different gyms', 'exploration', 5, 25, 'common', '\U0001F5FA'),
        ('gym_nomad', 'Gym Nomad', 'Visit 10 different gyms', 'exploration', 10, 50, 'rare', '\U0001F9F3'),
    ]

    created_count = 0
    for key, name, desc, category, req_count, xp, rarity, icon in achievements_data:
        achievement, created = Achievement.objects.get_or_create(
            key=key,
            defaults={
                'name': name,
                'description': desc,
                'category': category,
                'required_count': req_count,
                'xp_reward': xp,
                'rarity': rarity,
                'icon': icon,
            }
        )
        if created:
            created_count += 1
            print(f"Created achievement: {name}")

    print(f"\nTotal created: {created_count}/{len(achievements_data)}")
    return created_count
