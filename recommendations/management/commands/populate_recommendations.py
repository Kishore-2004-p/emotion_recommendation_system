from django.core.management.base import BaseCommand
from recommendations.models import RecommendationItem

class Command(BaseCommand):
    help = 'Populate database with sample recommendations'

    def handle(self, *args, **kwargs):
        recommendations = [
            # Happy recommendations
            {
                'title': 'Listen to Uplifting Music',
                'description': 'Boost your mood with positive, energetic songs',
                'category': 'music',
                'content_url': 'https://www.youtube.com/watch?v=y6Sxv-sUYtM',
                'target_emotions': ['happy', 'neutral'],
                'popularity_score': 85
            },
            {
                'title': 'Watch Comedy Shows',
                'description': 'Enjoy stand-up comedy or funny sitcoms to keep smiling',
                'category': 'entertainment',
                'content_url': 'https://www.netflix.com/browse/genre/6548',
                'target_emotions': ['happy', 'neutral'],
                'popularity_score': 90
            },
            {
                'title': 'Go for a Walk',
                'description': 'Take a refreshing walk outside to maintain your positive energy',
                'category': 'activity',
                'content_url': 'https://www.health.com/fitness/walking-benefits',
                'target_emotions': ['happy', 'neutral'],
                'popularity_score': 80
            },
            
            # Sad recommendations
            {
                'title': 'Talk to a Friend',
                'description': 'Reach out to someone you trust and share how you feel',
                'category': 'social',
                'content_url': 'https://www.7cups.com/',
                'target_emotions': ['sad', 'fear'],
                'popularity_score': 95
            },
            {
                'title': 'Practice Gratitude',
                'description': 'Write down 3 things you\'re grateful for today',
                'category': 'wellness',
                'content_url': 'https://www.calm.com/blog/gratitude-practice',
                'target_emotions': ['sad', 'neutral'],
                'popularity_score': 75
            },
            {
                'title': 'Watch Inspirational Videos',
                'description': 'Find motivation through uplifting stories and speeches',
                'category': 'entertainment',
                'content_url': 'https://www.ted.com/topics/inspiration',
                'target_emotions': ['sad', 'fear'],
                'popularity_score': 88
            },
            
            # Angry recommendations
            {
                'title': 'Deep Breathing Exercise',
                'description': 'Calm your mind with 5 minutes of deep breathing',
                'category': 'wellness',
                'content_url': 'https://www.headspace.com/breathing-exercises',
                'target_emotions': ['angry', 'fear'],
                'popularity_score': 92
            },
            {
                'title': 'Physical Exercise',
                'description': 'Channel your energy into a workout or sports activity',
                'category': 'activity',
                'content_url': 'https://www.youtube.com/results?search_query=home+workout',
                'target_emotions': ['angry', 'sad'],
                'popularity_score': 85
            },
            {
                'title': 'Meditation Session',
                'description': 'Practice mindfulness to regain emotional balance',
                'category': 'wellness',
                'content_url': 'https://www.calm.com/',
                'target_emotions': ['angry', 'fear', 'neutral'],
                'popularity_score': 90
            },
            
            # Fear/Anxiety recommendations
            {
                'title': 'Guided Relaxation',
                'description': 'Listen to calming guided meditation for anxiety relief',
                'category': 'wellness',
                'content_url': 'https://www.youtube.com/watch?v=inpok4MKVLM',
                'target_emotions': ['fear', 'sad'],
                'popularity_score': 87
            },
            {
                'title': 'Read Positive Affirmations',
                'description': 'Boost your confidence with empowering statements',
                'category': 'wellness',
                'content_url': 'https://www.mindful.org/daily-affirmations/',
                'target_emotions': ['fear', 'sad'],
                'popularity_score': 78
            },
            {
                'title': 'Progressive Muscle Relaxation',
                'description': 'Release tension through systematic muscle relaxation',
                'category': 'wellness',
                'content_url': 'https://www.verywellmind.com/how-to-relax-your-muscles-3024400',
                'target_emotions': ['fear', 'angry'],
                'popularity_score': 82
            },
            
            # Neutral recommendations
            {
                'title': 'Learn Something New',
                'description': 'Try a new skill or hobby to engage your mind',
                'category': 'education',
                'content_url': 'https://www.coursera.org/',
                'target_emotions': ['neutral', 'happy'],
                'popularity_score': 80
            },
            {
                'title': 'Listen to Podcasts',
                'description': 'Explore interesting topics through popular podcasts',
                'category': 'entertainment',
                'content_url': 'https://www.spotify.com/us/genre/podcasts-web/',
                'target_emotions': ['neutral'],
                'popularity_score': 75
            },
            {
                'title': 'Journaling',
                'description': 'Write down your thoughts and reflect on your day',
                'category': 'wellness',
                'content_url': 'https://penzu.com/',
                'target_emotions': ['neutral', 'sad'],
                'popularity_score': 70
            },
            
            # Surprise recommendations
            {
                'title': 'Explore New Music Genres',
                'description': 'Discover music styles you\'ve never tried before',
                'category': 'music',
                'content_url': 'https://www.spotify.com/',
                'target_emotions': ['surprise', 'happy'],
                'popularity_score': 77
            },
        ]

        created_count = 0
        for rec_data in recommendations:
            item, created = RecommendationItem.objects.get_or_create(
                title=rec_data['title'],
                defaults=rec_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {item.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Already exists: {item.title}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Total created: {created_count}/{len(recommendations)}'))
