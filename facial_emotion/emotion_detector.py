import cv2
import numpy as np
import os
from deepface import DeepFace

class FacialEmotionDetector:
    def __init__(self):
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        # Load face cascade for face detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier!")
        
        print("✓ Facial emotion detector initialized with DeepFace")
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(48, 48)
            )
            
            return faces
        except Exception as e:
            print(f"Face detection error: {e}")
            return []
    
    def predict_emotion(self, face_img):
        """Predict emotion using DeepFace"""
        try:
            # Analyze using DeepFace
            result = DeepFace.analyze(
                face_img,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            # Extract emotion data
            if isinstance(result, list):
                result = result[0]
            
            emotion_scores = result['emotion']
            dominant_emotion = result['dominant_emotion']
            confidence = emotion_scores[dominant_emotion] / 100.0
            
            # Normalize scores to 0-1 range
            all_predictions = {
                emotion.lower(): float(score / 100.0)
                for emotion, score in emotion_scores.items()
            }
            
            return str(dominant_emotion), float(confidence), all_predictions
            
        except Exception as e:
            print(f"DeepFace prediction error: {e}")
            return None, 0.0, {}
    
    def process_frame(self, frame):
        """Process single frame and return results"""
        results = []
        
        # Detect faces using cascade
        faces = self.detect_faces(frame)
        
        print(f"Detected {len(faces)} face(s)")
        
        if len(faces) == 0:
            # If no face detected by cascade, try DeepFace directly on whole frame
            try:
                print("No faces found by cascade, trying DeepFace on full frame...")
                emotion, confidence, all_preds = self.predict_emotion(frame)
                
                if emotion:
                    results.append({
                        'emotion': emotion,
                        'confidence': confidence,
                        'all_predictions': all_preds,
                        'coordinates': {
                            'x': 0,
                            'y': 0,
                            'width': frame.shape[1],
                            'height': frame.shape[0]
                        }
                    })
            except Exception as e:
                print(f"Full frame analysis error: {e}")
        else:
            # Process each detected face
            for (x, y, w, h) in faces:
                face_roi = frame[y:y+h, x:x+w]
                
                if face_roi.size == 0:
                    continue
                
                emotion, confidence, all_preds = self.predict_emotion(face_roi)
                
                if emotion:
                    results.append({
                        'emotion': emotion,
                        'confidence': confidence,
                        'all_predictions': all_preds,
                        'coordinates': {
                            'x': int(x),
                            'y': int(y),
                            'width': int(w),
                            'height': int(h)
                        }
                    })
        
        return results
