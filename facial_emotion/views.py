from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import cv2
import numpy as np
import traceback

from .models import FacialEmotionCapture

@login_required
def detect_view(request):
    """Facial emotion detection page"""
    return render(request, 'facial_emotion/detect.html')

@csrf_exempt
@login_required
def detect_emotion_api(request):
    """API endpoint for emotion detection"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'POST method required'}, status=405)
    
    try:
        print("="*50)
        print("EMOTION DETECTION API CALLED")
        print("="*50)
        
        # Get image data
        data = json.loads(request.body)
        image_data = data.get('image')
        
        if not image_data:
            return JsonResponse({'success': False, 'message': 'No image provided'}, status=400)
        
        print(f"Image data length: {len(image_data)}")
        
        # Decode image
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return JsonResponse({'success': False, 'message': 'Invalid image data'})
        
        print(f"Image decoded successfully. Shape: {frame.shape}")
        
        # Initialize detector
        from .emotion_detector import FacialEmotionDetector
        detector = FacialEmotionDetector()
        print("Detector initialized successfully")
        
        # Process frame
        results = detector.process_frame(frame)
        print(f"Detection complete. Found {len(results)} face(s)")
        
        if results and len(results) > 0:
            result = results[0]
            
            # Convert numpy types to Python native types
            emotion = str(result['emotion'])
            confidence = float(result['confidence'])
            all_predictions = {k: float(v) for k, v in result['all_predictions'].items()}
            
            # Save to database
            try:
                from .models import FacialEmotionCapture, FacialEmotionSession
                import uuid
                
                session_id = request.session.get('facial_emotion_session')
                if not session_id:
                    session_id = str(uuid.uuid4())
                    request.session['facial_emotion_session'] = session_id
                    session = FacialEmotionSession.objects.create(
                        user=request.user,
                        session_id=session_id
                    )
                else:
                    session = FacialEmotionSession.objects.filter(
                        session_id=session_id,
                        user=request.user
                    ).first()
                    if not session:
                        session = FacialEmotionSession.objects.create(
                            user=request.user,
                            session_id=session_id
                        )
                
                FacialEmotionCapture.objects.create(
                    session=session,
                    user=request.user,
                    detected_emotion=emotion,
                    confidence_score=confidence * 100,
                    all_predictions=all_predictions
                )
                print("✅ Saved to database successfully")
            except Exception as db_error:
                print(f"⚠️ Database save error: {db_error}")
            
            print(f"✅ Returning result: {emotion} ({confidence*100:.1f}%)")
            
            return JsonResponse({
                'success': True,
                'emotion': emotion,
                'confidence': round(confidence * 100, 2),
                'all_predictions': {k: round(v * 100, 2) for k, v in all_predictions.items()}
            })
        else:
            print("❌ No faces detected")
            return JsonResponse({
                'success': False,
                'message': 'No face detected. Please ensure your face is visible and well-lit.'
            })
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


@login_required
def history_view(request):
    """Facial emotion history page"""
    captures = FacialEmotionCapture.objects.filter(user=request.user).order_by('-captured_at')[:50]
    return render(request, 'facial_emotion/history.html', {'captures': captures})
