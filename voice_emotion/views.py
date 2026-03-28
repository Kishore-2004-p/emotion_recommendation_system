from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib import messages
from .models import VoiceEmotionAnalysis
import os
import json
import traceback

@login_required
def analyze_view(request):
    """Voice emotion analysis page - handles both GET and POST"""
    
    if request.method == 'POST':
        # Handle file upload
        try:
            print("="*50)
            print("VOICE ANALYSIS POST REQUEST")
            print("="*50)
            
            # Check if file was uploaded
            if 'audio_file' not in request.FILES:
                messages.error(request, 'No audio file uploaded')
                return redirect('voice_emotion:analyze')
            
            audio_file = request.FILES['audio_file']
            print(f"✓ Received file: {audio_file.name}")
            print(f"✓ File size: {audio_file.size} bytes")
            print(f"✓ Content type: {audio_file.content_type}")
            
            # Save file
            file_path = default_storage.save(f'voice_uploads/{audio_file.name}', audio_file)
            full_path = default_storage.path(file_path)
            print(f"✓ Saved to: {full_path}")
            
            # Analyze with AssemblyAI
            try:
                from .analyzer import VoiceEmotionAnalyzer  # Import from analyzer.py (not voice_analyzer.py)
                analyzer = VoiceEmotionAnalyzer()
                print("✓ AssemblyAI analyzer initialized")
                
                # Call the correct method name: analyze_emotion (not analyze_audio)
                result = analyzer.analyze_emotion(full_path)
                print(f"✓ Analysis result: {result}")
                
                if result and 'emotion' in result:
                    emotion = result['emotion']
                    confidence = result.get('confidence', 0.0) * 100  # Convert to percentage
                    all_predictions = result.get('all_predictions', {})
                    # Convert all predictions to percentages
                    all_predictions = {k: v * 100 if v < 1 else v for k, v in all_predictions.items()}
                else:
                    raise Exception("No emotion detected")
                    
            except Exception as analyzer_error:
                print(f"⚠️ Analyzer error: {analyzer_error}")
                traceback.print_exc()
                messages.error(request, f'Analysis failed: {str(analyzer_error)}')
                return redirect('voice_emotion:analyze')
            
            # Save to database
            try:
                analysis = VoiceEmotionAnalysis.objects.create(
                    user=request.user,
                    audio_file=file_path,
                    detected_emotion=emotion,
                    confidence_score=confidence,
                    all_predictions=all_predictions
                )
                print(f"✅ Saved to database: ID {analysis.id}")
                messages.success(request, f'Audio analyzed! Emotion: {emotion.upper()} ({confidence:.1f}%)')
                return redirect('voice_emotion:history')
                
            except Exception as db_error:
                print(f"❌ Database error: {db_error}")
                traceback.print_exc()
                messages.error(request, f'Database error: {str(db_error)}')
                return redirect('voice_emotion:analyze')
                
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            traceback.print_exc()
            messages.error(request, f'Error: {str(e)}')
            return redirect('voice_emotion:analyze')
    
    # GET request - show the analysis page
    return render(request, 'voice_emotion/analyze.html')


@login_required
def history_view(request):
    """Voice emotion history page"""
    analyses = VoiceEmotionAnalysis.objects.filter(user=request.user).order_by('-analyzed_at')[:50]
    print(f"Loading history: Found {analyses.count()} analyses for user {request.user.username}")
    return render(request, 'voice_emotion/history.html', {'analyses': analyses})


@csrf_exempt
@login_required
def analyze_emotion_api(request):
    """API endpoint for voice emotion analysis (for AJAX/recorded audio)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'POST method required'}, status=405)
    
    try:
        print("="*50)
        print("VOICE EMOTION ANALYSIS API CALLED")
        print("="*50)
        
        # Check if file was uploaded
        if 'audio_file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'message': 'No audio file provided'
            }, status=400)
        
        audio_file = request.FILES['audio_file']
        print(f"Received file: {audio_file.name}")
        print(f"File size: {audio_file.size} bytes")
        print(f"Content type: {audio_file.content_type}")
        
        # Save file
        file_path = default_storage.save(f'voice_uploads/{audio_file.name}', audio_file)
        full_path = default_storage.path(file_path)
        print(f"Saved to: {full_path}")
        
        # Analyze with AssemblyAI
        try:
            from .analyzer import VoiceEmotionAnalyzer
            analyzer = VoiceEmotionAnalyzer()
            print("✓ AssemblyAI analyzer initialized")
            
            result = analyzer.analyze_emotion(full_path)
            print(f"Analysis result: {result}")
            
            if result and 'emotion' in result:
                emotion = result['emotion']
                confidence = result.get('confidence', 0.0) * 100
                all_predictions = result.get('all_predictions', {})
                all_predictions = {k: v * 100 if v < 1 else v for k, v in all_predictions.items()}
            else:
                raise Exception("No emotion detected")
                
        except Exception as analyzer_error:
            print(f"⚠️ Analyzer error: {analyzer_error}")
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'message': f'Analysis failed: {str(analyzer_error)}'
            })
        
        # Save to database
        try:
            VoiceEmotionAnalysis.objects.create(
                user=request.user,
                audio_file=file_path,
                detected_emotion=emotion,
                confidence_score=confidence,
                all_predictions=all_predictions
            )
            print("✅ Saved to database successfully")
        except Exception as db_error:
            print(f"⚠️ Database save error: {db_error}")
        
        print(f"✅ Returning result: {emotion} ({confidence:.1f}%)")
        
        return JsonResponse({
            'success': True,
            'emotion': emotion,
            'confidence': round(confidence, 2),
            'all_predictions': {k: round(v, 2) for k, v in all_predictions.items()}
        })
                
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)
