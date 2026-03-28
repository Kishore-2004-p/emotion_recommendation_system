import cv2
import numpy as np
from tensorflow import keras
import os
from django.conf import settings

class FacialEmotionDetector:
    def __init__(self):
        # Use .hdf5 extension
        model_path = os.path.join(settings.BASE_DIR, 'facial_emotion', 'ml_models', 'facial_emotion_model.h5')
        
        # Check if model exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")
        
        print(f"Loading model from: {model_path}")
        self.model = keras.models.load_model(model_path)
        self.emotion_labels = settings.EMOTION_CLASSES
        
        # Print model input shape for debugging
        print(f"Model input shape: {self.model.input_shape}")
        
        # Load face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier!")
        
        print("FacialEmotionDetector initialized successfully")
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(48, 48)
        )
        
        return faces
    
    def predict_emotion(self, face_img):
        """Predict emotion from face image"""
        try:
            # Preprocess - resize to 48x48
            face_img = cv2.resize(face_img, (48, 48))
            
            # Convert to grayscale if not already
            if len(face_img.shape) == 3:
                face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            
            # Normalize to [0, 1]
            face_img = face_img.astype('float32') / 255.0
            
            # Reshape to match model input: (1, 48, 48, 1)
            # This is the correct 4D shape for Conv2D
            face_img = face_img.reshape(1, 48, 48, 1)
            
            print(f"Input shape to model: {face_img.shape}")
            
            # Predict
            predictions = self.model.predict(face_img, verbose=0)[0]
            emotion_idx = np.argmax(predictions)
            emotion = self.emotion_labels[emotion_idx]
            confidence = float(predictions[emotion_idx])
            
            # All predictions as dict
            all_predictions = {
                self.emotion_labels[i]: float(predictions[i]) 
                for i in range(len(self.emotion_labels))
            }
            
            return emotion, confidence, all_predictions
            
        except Exception as e:
            print(f"Error in emotion prediction: {e}")
            import traceback
            traceback.print_exc()
            return None, 0.0, {}
    
    def process_frame(self, frame):
        """Process single frame and return results"""
        faces = self.detect_faces(frame)
        results = []
        
        print(f"Detected {len(faces)} face(s)")
        
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
