from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class VoiceEmotionAnalysis(models.Model):
    VOICE_EMOTION_CHOICES = [(emotion, emotion.capitalize()) for emotion in settings.VOICE_EMOTIONS]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_analyses')
    
    audio_file = models.FileField(upload_to='voice_samples/')
    detected_emotion = models.CharField(max_length=20, choices=VOICE_EMOTION_CHOICES)
    confidence_score = models.FloatField()
    
    # Audio features
    pitch_mean = models.FloatField(blank=True, null=True)
    pitch_std = models.FloatField(blank=True, null=True)
    energy_mean = models.FloatField(blank=True, null=True)
    speaking_rate = models.FloatField(blank=True, null=True)
    
    all_predictions = models.JSONField(default=dict)
    audio_duration = models.FloatField(default=0.0)
    
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'voice_emotion_analyses'
        ordering = ['-analyzed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.detected_emotion} ({self.confidence_score:.2f})"
