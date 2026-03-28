import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emotion_project.settings')
django.setup()

from recommendations.models import RecommendationItem

# Sample recommendations data
recommendations_data = [
    # Happy emotion
    {
        'title': 'Uplifting Pop Playlist',
        'description': 'Feel-good music to boost your mood',
        'category': 'music',
        'content_url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
        'target_emotions': ['happy', 'neutral'],
        'tags': ['music', 'pop', 'energetic'],
        'popularity_score': 8.5
    },
    {
        'title': 'Comedy Movie Collection',
        'description': 'Laugh out loud with these comedy classics',
        'category': 'video',
        'content_url': 'https://www.netflix.com/browse/genre/6548',
        'target_emotions': ['happy', 'neutral'],
        'tags': ['movies', 'comedy', 'entertainment'],
        'popularity_score': 9.0
    },
    
    # Sad emotion
    {
        'title': 'Calming Meditation Guide',
        'description': 'Guided meditation to find inner peace',
        'category': 'activity',
        'content_url': 'https://www.headspace.com',
        'target_emotions': ['sad', 'angry', 'fear'],
        'tags': ['meditation', 'wellness', 'mental health'],
        'popularity_score': 9.2
    },
    {
        'title': 'Motivational Articles',
        'description': 'Inspiring stories to lift your spirits',
        'category': 'article',
        'content_url': 'https://www.psychologytoday.com/motivation',
        'target_emotions': ['sad', 'neutral'],
        'tags': ['motivation', 'self-help', 'inspiration'],
        'popularity_score': 7.8
    },
    
    # Angry emotion
    {
        'title': 'Stress Relief Exercise Routines',
        'description': 'Physical activities to release tension',
        'category': 'activity',
        'content_url': 'https://www.youtube.com/results?search_query=stress+relief+workout',
        'target_emotions': ['angry', 'fear'],
        'tags': ['fitness', 'stress relief', 'workout'],
        'popularity_score': 8.0
    },
    {
        'title': 'Anger Management Course',
        'description': 'Learn techniques to manage emotions effectively',
        'category': 'course',
        'content_url': 'https://www.coursera.org/courses?query=anger%20management',
        'target_emotions': ['angry'],
        'tags': ['education', 'self-improvement', 'psychology'],
        'popularity_score': 7.5
    },
    
    # Fear/Anxious
    {
        'title': 'Relaxing Nature Sounds',
        'description': 'Peaceful sounds to calm your mind',
        'category': 'music',
        'content_url': 'https://www.calm.com',
        'target_emotions': ['fear', 'sad', 'angry'],
        'tags': ['relaxation', 'nature', 'ambient'],
        'popularity_score': 8.8
    },
    {
        'title': 'Anxiety Relief Techniques',
        'description': 'Practical strategies to manage anxiety',
        'category': 'article',
        'content_url': 'https://www.anxietycanada.com',
        'target_emotions': ['fear'],
        'tags': ['mental health', 'anxiety', 'coping strategies'],
        'popularity_score': 9.1
    },
    
    # Neutral/General
    {
        'title': 'Productivity Tools Collection',
        'description': 'Boost your efficiency with these tools',
        'category': 'product',
        'content_url': 'https://www.notion.so',
        'target_emotions': ['neutral', 'happy'],
        'tags': ['productivity', 'tools', 'organization'],
        'popularity_score': 8.3
    },
    {
        'title': 'Educational Documentaries',
        'description': 'Expand your knowledge with fascinating docs',
        'category': 'video',
        'content_url': 'https://www.curiositystream.com',
        'target_emotions': ['neutral', 'happy'],
        'tags': ['education', 'documentary', 'learning'],
        'popularity_score': 8.6
    },
    
    # Surprise emotion
    {
        'title': 'Adventure Activity Ideas',
        'description': 'Try something new and exciting',
        'category': 'activity',
        'content_url': 'https://www.airbnb.com/s/experiences',
        'target_emotions': ['surprise', 'happy', 'neutral'],
        'tags': ['adventure', 'travel', 'experiences'],
        'popularity_score': 8.4
    },
    {
        'title': 'Thrilling Mystery Movies',
        'description': 'Keep you on the edge of your seat',
        'category': 'video',
        'content_url': 'https://www.imdb.com/search/title/?genres=mystery',
        'target_emotions': ['surprise', 'happy'],
        'tags': ['movies', 'mystery', 'thriller'],
        'popularity_score': 8.7
    },
    
    # Disgust emotion  
    {
        'title': 'Mindfulness and Grounding Exercises',
        'description': 'Return to a centered state of mind',
        'category': 'activity',
        'content_url': 'https://www.mindful.org/meditation/mindfulness-getting-started',
        'target_emotions': ['disgust', 'angry', 'fear'],
        'tags': ['mindfulness', 'grounding', 'wellness'],
        'popularity_score': 7.9
    },
    {
        'title': 'Positive Psychology Resources',
        'description': 'Focus on the good in life',
        'category': 'article',
        'content_url': 'https://positivepsychology.com',
        'target_emotions': ['disgust', 'sad', 'neutral'],
        'tags': ['psychology', 'positivity', 'well-being'],
        'popularity_score': 8.1
    },
]

# Clear existing data
RecommendationItem.objects.all().delete()

# Create recommendations
for data in recommendations_data:
    RecommendationItem.objects.create(**data)
    print(f"Created: {data['title']}")

print(f"\n✓ Successfully created {len(recommendations_data)} recommendation items!")
