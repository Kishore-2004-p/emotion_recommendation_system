from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from facial_emotion.models import FacialEmotionCapture, FacialEmotionSession
from voice_emotion.models import VoiceEmotionAnalysis
from recommendations.models import UserRecommendation, UserFeedback
from recommendations.recommendation_engine import RecommendationEngine
from datetime import datetime, timedelta
from collections import Counter
import json

@login_required
def user_dashboard(request):
    """Enhanced user dashboard with statistics and charts"""
    user = request.user
    
    # Get recommendation engine
    try:
        engine = RecommendationEngine(user)
        recommendations = engine.get_recommendations(limit=5)
    except:
        recommendations = []
    
    # Get emotion counts
    facial_count = FacialEmotionCapture.objects.filter(user=user).count()
    voice_count = VoiceEmotionAnalysis.objects.filter(user=user).count()
    total_detections = facial_count + voice_count
    
    # Get recent emotions (last 10)
    recent_facial = FacialEmotionCapture.objects.filter(user=user).order_by('-captured_at')[:5]
    recent_voice = VoiceEmotionAnalysis.objects.filter(user=user).order_by('-analyzed_at')[:5]
    
    recent_emotions = []
    for capture in recent_facial:
        recent_emotions.append({
            'type': 'facial',
            'emotion': capture.detected_emotion,
            'confidence': capture.confidence_score,
            'timestamp': capture.captured_at
        })
    
    for analysis in recent_voice:
        recent_emotions.append({
            'type': 'voice',
            'emotion': analysis.detected_emotion,
            'confidence': analysis.confidence_score,
            'timestamp': analysis.analyzed_at
        })
    
    # Sort by timestamp
    recent_emotions = sorted(recent_emotions, key=lambda x: x['timestamp'], reverse=True)[:10]
    
    # Get emotion distribution
    all_facial = list(FacialEmotionCapture.objects.filter(user=user).values_list('detected_emotion', flat=True))
    all_voice = list(VoiceEmotionAnalysis.objects.filter(user=user).values_list('detected_emotion', flat=True))
    all_emotions = all_facial + all_voice
    
    emotion_distribution = dict(Counter(all_emotions))
    dominant_emotion = max(emotion_distribution, key=emotion_distribution.get).title() if emotion_distribution else 'N/A'
    
    # Average confidence
    avg_facial_conf = FacialEmotionCapture.objects.filter(user=user).aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    avg_voice_conf = VoiceEmotionAnalysis.objects.filter(user=user).aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    avg_confidence = round((avg_facial_conf + avg_voice_conf) / 2, 1) if (avg_facial_conf or avg_voice_conf) else 0
    
    # Last 7 days activity
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_activity = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).date()
        day_facial = FacialEmotionCapture.objects.filter(user=user, captured_at__date=date).count()
        day_voice = VoiceEmotionAnalysis.objects.filter(user=user, analyzed_at__date=date).count()
        recent_activity.append({
            'date': date.strftime('%m/%d'),
            'facial': day_facial,
            'voice': day_voice,
            'total': day_facial + day_voice
        })
    recent_activity.reverse()
    
    # Chart data
    emotion_labels = list(emotion_distribution.keys())
    emotion_values = list(emotion_distribution.values())
    
    context = {
        'recommendations': recommendations,
        'recent_emotions': recent_emotions,
        'facial_count': facial_count,
        'voice_count': voice_count,
        'total_detections': total_detections,
        'dominant_emotion': dominant_emotion,
        'avg_confidence': avg_confidence,
        'emotion_distribution': emotion_distribution,
        'emotion_labels_json': json.dumps(emotion_labels),
        'emotion_values_json': json.dumps(emotion_values),
        'recent_activity': recent_activity,
    }
    return render(request, 'user_dashboard/dashboard.html', context)

@login_required
def user_emotion_history(request):
    """User's emotion history with filtering"""
    user = request.user
    
    # Get filter parameter
    filter_type = request.GET.get('type', 'all')
    date_filter = request.GET.get('date', 'all')
    
    # Base querysets
    facial_emotions = FacialEmotionCapture.objects.filter(user=user)
    voice_emotions = VoiceEmotionAnalysis.objects.filter(user=user)
    
    # Apply date filter
    if date_filter == 'today':
        today = datetime.now().date()
        facial_emotions = facial_emotions.filter(captured_at__date=today)
        voice_emotions = voice_emotions.filter(analyzed_at__date=today)
    elif date_filter == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        facial_emotions = facial_emotions.filter(captured_at__gte=week_ago)
        voice_emotions = voice_emotions.filter(analyzed_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = datetime.now() - timedelta(days=30)
        facial_emotions = facial_emotions.filter(captured_at__gte=month_ago)
        voice_emotions = voice_emotions.filter(analyzed_at__gte=month_ago)
    
    # Apply type filter
    if filter_type == 'facial':
        voice_emotions = VoiceEmotionAnalysis.objects.none()
    elif filter_type == 'voice':
        facial_emotions = FacialEmotionCapture.objects.none()
    
    facial_emotions = facial_emotions.order_by('-captured_at')[:50]
    voice_emotions = voice_emotions.order_by('-analyzed_at')[:50]
    
    # Statistics
    total_facial = FacialEmotionCapture.objects.filter(user=user).count()
    total_voice = VoiceEmotionAnalysis.objects.filter(user=user).count()
    
    return render(request, 'user_dashboard/emotions.html', {
        'facial_emotions': facial_emotions,
        'voice_emotions': voice_emotions,
        'filter_type': filter_type,
        'date_filter': date_filter,
        'total_facial': total_facial,
        'total_voice': total_voice,
    })

@login_required
def user_recommendations(request):
    """User's recommendations page"""
    recommendations = UserRecommendation.objects.filter(
        user=request.user
    ).order_by('-recommended_at')[:20]
    
    # Statistics
    total_recommendations = UserRecommendation.objects.filter(user=request.user).count()
    
    return render(request, 'user_dashboard/recommendations.html', {
        'recommendations': recommendations,
        'total_recommendations': total_recommendations,
    })

@login_required
def user_feedback_history(request):
    """User's feedback history"""
    feedbacks = UserFeedback.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Statistics
    total_feedback = feedbacks.count()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'user_dashboard/feedback.html', {
        'feedbacks': feedbacks,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 1),
    })
