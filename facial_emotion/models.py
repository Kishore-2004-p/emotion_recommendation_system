from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class FacialEmotionSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facial_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'facial_emotion_sessions'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_id}"

class FacialEmotionCapture(models.Model):
    EMOTION_CHOICES = [(emotion, emotion.capitalize()) for emotion in settings.EMOTION_CLASSES]
    
    session = models.ForeignKey(FacialEmotionSession, on_delete=models.CASCADE, related_name='captures')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facial_captures')
    
    detected_emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    confidence_score = models.FloatField()
    
    image_snapshot = models.ImageField(upload_to='emotion_captures/', blank=True, null=True)
    face_coordinates = models.JSONField(default=dict)  # {x, y, width, height}
    
    all_predictions = models.JSONField(default=dict)  # All emotion probabilities
    
    captured_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'facial_emotion_captures'
        ordering = ['-captured_at']
        indexes = [
            models.Index(fields=['-captured_at']),
            models.Index(fields=['user', '-captured_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.detected_emotion} ({self.confidence_score:.2f})"
