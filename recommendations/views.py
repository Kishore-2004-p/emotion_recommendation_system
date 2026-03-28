from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RecommendationItem, UserRecommendation, UserFeedback
from .recommendation_engine import RecommendationEngine

@login_required
def recommendations_list(request):
    """Display personalized recommendations"""
    engine = RecommendationEngine(request.user)
    recommendations = engine.get_recommendations(limit=10)
    return render(request, 'recommendations/list.html', {'recommendations': recommendations})

@login_required
def recommendation_history(request):
    """User's recommendation history"""
    history = UserRecommendation.objects.filter(user=request.user).order_by('-recommended_at')[:50]
    return render(request, 'recommendations/history.html', {'history': history})

@login_required
def feedback_view(request, item_id):
    """Submit feedback for a recommendation"""
    item = get_object_or_404(RecommendationItem, id=item_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        UserFeedback.objects.create(
            user=request.user,
            rating=rating,
            comment=comment,
            feedback_type='recommendation'
        )
        messages.success(request, 'Feedback submitted successfully!')
        return redirect('recommendations:list')
    return render(request, 'recommendations/feedback.html', {'item': item})
