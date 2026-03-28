from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from facial_emotion.models import FacialEmotionCapture, FacialEmotionSession
from voice_emotion.models import VoiceEmotionAnalysis
from recommendations.models import RecommendationItem, UserFeedback, UserRecommendation
from datetime import datetime, timedelta
from collections import Counter
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Enhanced admin dashboard with comprehensive statistics"""
    
    # User statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=datetime.now()-timedelta(days=7)).count()
    new_users_today = User.objects.filter(date_joined__date=datetime.now().date()).count()
    
    # Emotion detection statistics
    total_facial = FacialEmotionCapture.objects.count()
    total_voice = VoiceEmotionAnalysis.objects.count()
    total_emotions = total_facial + total_voice
    
    # Today's activity
    today = datetime.now().date()
    today_facial = FacialEmotionCapture.objects.filter(captured_at__date=today).count()
    today_voice = VoiceEmotionAnalysis.objects.filter(analyzed_at__date=today).count()
    today_total = today_facial + today_voice
    
    # Recommendation statistics
    total_recommendations = RecommendationItem.objects.filter(is_active=True).count()
    total_user_recommendations = UserRecommendation.objects.count()
    
    # Feedback statistics
    total_feedback = UserFeedback.objects.count()
    avg_rating = UserFeedback.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Emotion distribution (all users)
    facial_emotions = list(FacialEmotionCapture.objects.values_list('detected_emotion', flat=True))
    voice_emotions = list(VoiceEmotionAnalysis.objects.values_list('detected_emotion', flat=True))
    all_emotions = facial_emotions + voice_emotions
    
    emotion_distribution = dict(Counter(all_emotions))
    top_emotions = Counter(all_emotions).most_common(5)
    
    # Chart data
    emotion_labels = list(emotion_distribution.keys())
    emotion_values = list(emotion_distribution.values())
    
    # Last 7 days activity
    daily_activity = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).date()
        day_count = (
            FacialEmotionCapture.objects.filter(captured_at__date=date).count() +
            VoiceEmotionAnalysis.objects.filter(analyzed_at__date=date).count()
        )
        daily_activity.append({
            'date': date.strftime('%m/%d'),
            'count': day_count
        })
    daily_activity.reverse()
    
    # User activity leaderboard
    user_activity = []
    for user in User.objects.all()[:10]:
        facial_count = FacialEmotionCapture.objects.filter(user=user).count()
        voice_count = VoiceEmotionAnalysis.objects.filter(user=user).count()
        total = facial_count + voice_count
        if total > 0:
            user_activity.append({
                'username': user.username,
                'facial': facial_count,
                'voice': voice_count,
                'total': total
            })
    user_activity = sorted(user_activity, key=lambda x: x['total'], reverse=True)[:10]
    
    # Recent activity (all users)
    recent_facial = FacialEmotionCapture.objects.select_related('user').order_by('-captured_at')[:10]
    recent_voice = VoiceEmotionAnalysis.objects.select_related('user').order_by('-analyzed_at')[:10]
    
    recent_activity = []
    for capture in recent_facial:
        recent_activity.append({
            'type': 'facial',
            'user': capture.user.username,
            'emotion': capture.detected_emotion,
            'confidence': capture.confidence_score,
            'timestamp': capture.captured_at
        })
    
    for analysis in recent_voice:
        recent_activity.append({
            'type': 'voice',
            'user': analysis.user.username,
            'emotion': analysis.detected_emotion,
            'confidence': analysis.confidence_score,
            'timestamp': analysis.analyzed_at
        })
    
    recent_activity = sorted(recent_activity, key=lambda x: x['timestamp'], reverse=True)[:15]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users_today': new_users_today,
        'total_facial': total_facial,
        'total_voice': total_voice,
        'total_emotions': total_emotions,
        'today_facial': today_facial,
        'today_voice': today_voice,
        'today_total': today_total,
        'total_recommendations': total_recommendations,
        'total_user_recommendations': total_user_recommendations,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 2),
        'emotion_distribution': emotion_distribution,
        'top_emotions': top_emotions,
        'emotion_labels_json': json.dumps(emotion_labels),
        'emotion_values_json': json.dumps(emotion_values),
        'daily_activity': daily_activity,
        'user_activity': user_activity,
        'recent_activity': recent_activity,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    """Enhanced user management page"""
    users = User.objects.all().order_by('-date_joined')
    
    # Add statistics for each user
    user_data = []
    for user in users:
        facial_count = FacialEmotionCapture.objects.filter(user=user).count()
        voice_count = VoiceEmotionAnalysis.objects.filter(user=user).count()
        feedback_count = UserFeedback.objects.filter(user=user).count()
        
        user_data.append({
            'user': user,
            'facial_count': facial_count,
            'voice_count': voice_count,
            'feedback_count': feedback_count,
            'total_activity': facial_count + voice_count,
            'last_login': user.last_login,
            'is_active': user.is_active,
        })
    
    return render(request, 'admin_panel/users.html', {
        'user_data': user_data,
        'total_users': len(user_data),
    })

@login_required
@user_passes_test(is_admin)
def emotion_reports(request):
    """Emotion data reports with filtering"""
    filter_type = request.GET.get('type', 'all')
    date_filter = request.GET.get('date', 'all')
    
    # Base querysets
    facial_emotions = FacialEmotionCapture.objects.all()
    voice_emotions = VoiceEmotionAnalysis.objects.all()
    
    # Apply filters
    if date_filter == 'today':
        today = datetime.now().date()
        facial_emotions = facial_emotions.filter(captured_at__date=today)
        voice_emotions = voice_emotions.filter(analyzed_at__date=today)
    elif date_filter == 'week':
        week_ago = datetime.now() - timedelta(days=7)
        facial_emotions = facial_emotions.filter(captured_at__gte=week_ago)
        voice_emotions = voice_emotions.filter(analyzed_at__gte=week_ago)
    
    if filter_type == 'facial':
        voice_emotions = VoiceEmotionAnalysis.objects.none()
    elif filter_type == 'voice':
        facial_emotions = FacialEmotionCapture.objects.none()
    
    facial_emotions = facial_emotions.select_related('user').order_by('-captured_at')[:100]
    voice_emotions = voice_emotions.select_related('user').order_by('-analyzed_at')[:100]
    
    return render(request, 'admin_panel/emotions.html', {
        'facial_emotions': facial_emotions,
        'voice_emotions': voice_emotions,
        'filter_type': filter_type,
        'date_filter': date_filter,
    })

@login_required
@user_passes_test(is_admin)
def manage_recommendations(request):
    """Manage recommendation items"""
    items = RecommendationItem.objects.all().order_by('-created_at')
    
    # Statistics
    active_items = items.filter(is_active=True).count()
    inactive_items = items.filter(is_active=False).count()
    
    return render(request, 'admin_panel/recommendations.html', {
        'items': items,
        'active_items': active_items,
        'inactive_items': inactive_items,
    })

@login_required
@user_passes_test(is_admin)
def feedback_management(request):
    """View and manage user feedback"""
    feedbacks = UserFeedback.objects.all().order_by('-created_at')
    
    # Statistics
    total_feedback = feedbacks.count()
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
    rating_distribution = {
        5: feedbacks.filter(rating=5).count(),
        4: feedbacks.filter(rating=4).count(),
        3: feedbacks.filter(rating=3).count(),
        2: feedbacks.filter(rating=2).count(),
        1: feedbacks.filter(rating=1).count(),
    }
    
    return render(request, 'admin_panel/feedback.html', {
        'feedbacks': feedbacks,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 2),
        'rating_distribution': rating_distribution,
    })

@login_required
@user_passes_test(is_admin)
def analytics_view(request):
    """Advanced analytics and reports"""
    from collections import Counter
    
    # Total statistics
    total_facial = FacialEmotionCapture.objects.count()
    total_voice = VoiceEmotionAnalysis.objects.count()
    total_detections = total_facial + total_voice
    
    # Today's detections
    today = datetime.now().date()
    today_detections = (
        FacialEmotionCapture.objects.filter(captured_at__date=today).count() +
        VoiceEmotionAnalysis.objects.filter(analyzed_at__date=today).count()
    )
    
    # Percentages
    facial_percentage = round((total_facial / total_detections * 100) if total_detections > 0 else 0, 1)
    voice_percentage = round((total_voice / total_detections * 100) if total_detections > 0 else 0, 1)
    
    # Average confidence
    avg_facial_conf = FacialEmotionCapture.objects.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    avg_voice_conf = VoiceEmotionAnalysis.objects.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    avg_confidence = round((avg_facial_conf + avg_voice_conf) / 2, 1) if (avg_facial_conf or avg_voice_conf) else 0
    
    # Emotion trends over 30 days
    days = 30
    emotion_trends = []
    trend_labels = []
    trend_values = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).date()
        count = (
            FacialEmotionCapture.objects.filter(captured_at__date=date).count() +
            VoiceEmotionAnalysis.objects.filter(analyzed_at__date=date).count()
        )
        emotion_trends.append({
            'date': date.strftime('%m/%d'),
            'count': count
        })
        trend_labels.append(date.strftime('%m/%d'))
        trend_values.append(count)
    
    emotion_trends.reverse()
    trend_labels.reverse()
    trend_values.reverse()
    
    # Emotion distribution
    facial_emotions = list(FacialEmotionCapture.objects.values_list('detected_emotion', flat=True))
    voice_emotions = list(VoiceEmotionAnalysis.objects.values_list('detected_emotion', flat=True))
    all_emotions = facial_emotions + voice_emotions
    
    emotion_distribution = dict(Counter(all_emotions))
    top_emotions = Counter(all_emotions).most_common(7)
    
    # Prepare data for charts
    emotion_labels = list(emotion_distribution.keys())
    emotion_values = list(emotion_distribution.values())
    
    # Calculate percentages for top emotions
    top_emotions_with_percent = []
    for emotion, count in top_emotions:
        percentage = round((count / total_detections * 100) if total_detections > 0 else 0, 1)
        top_emotions_with_percent.append({
            'emotion': emotion,
            'count': count,
            'percentage': percentage
        })
    
    context = {
        'total_detections': total_detections,
        'total_facial': total_facial,
        'total_voice': total_voice,
        'today_detections': today_detections,
        'facial_percentage': facial_percentage,
        'voice_percentage': voice_percentage,
        'avg_confidence': avg_confidence,
        'emotion_trends': emotion_trends,
        'trend_labels': json.dumps(trend_labels),
        'trend_values': json.dumps(trend_values),
        'emotion_distribution': emotion_distribution,
        'emotion_labels': json.dumps(emotion_labels),
        'emotion_values': json.dumps(emotion_values),
        'top_emotions': top_emotions,
        'top_emotions_with_percent': top_emotions_with_percent,
    }
    
    return render(request, 'admin_panel/analytics.html', context)
