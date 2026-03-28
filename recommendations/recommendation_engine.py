from .models import RecommendationItem, UserRecommendation
from facial_emotion.models import FacialEmotionCapture
from voice_emotion.models import VoiceEmotionAnalysis
from datetime import timedelta
from django.utils import timezone
import random


class RecommendationEngine:

    def __init__(self, user):
        self.user = user

    def get_recent_emotions(self, days=7):
        """Get user's recent emotional state"""

        since = timezone.now() - timedelta(days=days)

        # Facial emotions
        facial_emotions = list(
            FacialEmotionCapture.objects.filter(
                user=self.user,
                captured_at__gte=since
            ).values_list('detected_emotion', flat=True)
        )

        # Voice emotions
        voice_emotions = list(
            VoiceEmotionAnalysis.objects.filter(
                user=self.user,
                analyzed_at__gte=since
            ).values_list('detected_emotion', flat=True)
        )

        all_emotions = facial_emotions + voice_emotions

        if not all_emotions:
            return ['neutral']

        # Count frequency
        emotion_counts = {}

        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        sorted_emotions = sorted(
            emotion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [emotion for emotion, _ in sorted_emotions[:3]]

    def get_recommendations(self, emotion=None, limit=10):
        """SQLite compatible recommendation system"""

        if emotion is None:
            recent_emotions = self.get_recent_emotions()
            primary_emotion = recent_emotions[0]
        else:
            primary_emotion = emotion
            recent_emotions = [emotion]

        # Get all active items
        all_items = RecommendationItem.objects.filter(
            is_active=True
        ).order_by('-popularity_score')

        matched_items = []

        # Manual filtering (SQLite safe)
        for item in all_items:

            target_emotions = item.target_emotions or []

            if primary_emotion in target_emotions:
                matched_items.append(item)

            elif any(
                em in target_emotions
                for em in recent_emotions
            ):
                matched_items.append(item)

        matched_items = matched_items[:limit * 2]

        scored_items = []

        for item in matched_items:

            relevance = self._calculate_relevance(
                item,
                primary_emotion,
                recent_emotions
            )

            scored_items.append((item, relevance))

        # Sort by relevance
        scored_items.sort(
            key=lambda x: x[1],
            reverse=True
        )

        final_recommendations = []

        for item, relevance in scored_items[:limit]:

            rec = UserRecommendation.objects.create(
                user=self.user,
                item=item,
                emotion_context=primary_emotion,
                relevance_score=relevance
            )

            final_recommendations.append(rec)

        return final_recommendations

    def _calculate_relevance(
        self,
        item,
        primary_emotion,
        recent_emotions
    ):

        score = 0.0

        if primary_emotion in item.target_emotions:
            score += 50

        for emotion in recent_emotions:
            if emotion in item.target_emotions:
                score += 20

        score += item.popularity_score * 2

        try:
            profile = self.user.profile

            if profile.preferred_categories:
                if item.category in profile.preferred_categories:
                    score += 30

        except:
            pass

        score += random.uniform(0, 10)

        return round(score, 2)