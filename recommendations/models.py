from django.db import models
from django.contrib.auth.models import User

class RecommendationItem(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('video', 'Video'),
        ('article', 'Article'),
        ('product', 'Product'),
        ('activity', 'Activity'),
        ('course', 'Course'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True)
    content_url = models.URLField()
    
    # Emotion mapping (which emotions this item suits)
    target_emotions = models.JSONField(default=list)  # ['happy', 'calm']
    
    tags = models.JSONField(default=list)
    popularity_score = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'recommendation_items'
        ordering = ['-popularity_score']
    
    def __str__(self):
        return self.title

class UserRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    item = models.ForeignKey(RecommendationItem, on_delete=models.CASCADE)
    
    emotion_context = models.CharField(max_length=20)  # Emotion when recommended
    relevance_score = models.FloatField()
    
    recommended_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_recommendations'
        ordering = ['-recommended_at']

class UserFeedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    recommendation = models.ForeignKey(UserRecommendation, on_delete=models.CASCADE, null=True, blank=True)
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    feedback_type = models.CharField(max_length=50, default='recommendation')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_feedbacks'
        ordering = ['-created_at']
