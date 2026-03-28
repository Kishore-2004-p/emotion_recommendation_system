import assemblyai as aai
import os

class VoiceEmotionAnalyzer:
    def __init__(self):
        # Get API key from environment or use your key
        api_key = os.environ.get('ASSEMBLYAI_API_KEY', 'd6c22164eb964d8085f9936639045dce')
        aai.settings.api_key = api_key
        
        self.transcriber = aai.Transcriber()
        print("✓ Voice emotion analyzer initialized with AssemblyAI")
        print(f"✓ API key configured: {api_key[:10]}...")
    
    def analyze_emotion(self, audio_path):
        """Analyze emotion using AssemblyAI"""
        try:
            print(f"Analyzing: {audio_path}")
            print(f"File size: {os.path.getsize(audio_path)} bytes")
            
            # Configure transcription with sentiment analysis
            config = aai.TranscriptionConfig(
                sentiment_analysis=True,
                language_code="en"
            )
            
            # Transcribe audio
            print("Uploading and transcribing audio...")
            transcript = self.transcriber.transcribe(audio_path, config)
            
            # Check transcript status
            print(f"Transcript status: {transcript.status}")
            
            if transcript.status == aai.TranscriptStatus.error:
                print(f"Transcription error: {transcript.error}")
                return None
            
            # Get text
            text = transcript.text
            print(f"Transcribed text: {text[:100]}...")
            
            # Get sentiment analysis
            sentiments = []
            if hasattr(transcript, 'sentiment_analysis') and transcript.sentiment_analysis:
                sentiments = transcript.sentiment_analysis
            
            if sentiments and len(sentiments) > 0:
                # Get overall sentiment
                sentiment_counts = {'POSITIVE': 0, 'NEGATIVE': 0, 'NEUTRAL': 0}
                
                for sent in sentiments:
                    sentiment_counts[sent.sentiment] += 1
                
                # Determine dominant sentiment
                dominant = max(sentiment_counts, key=sentiment_counts.get)
                confidence = sentiment_counts[dominant] / len(sentiments)
                
                # Map to emotions
                emotion_map = {
                    'POSITIVE': 'happy',
                    'NEGATIVE': 'sad',
                    'NEUTRAL': 'neutral'
                }
                
                emotion = emotion_map.get(dominant, 'neutral')
                
                print(f"✓ Detected emotion: {emotion} (confidence: {confidence:.2%})")
                
                return {
                    'emotion': emotion,
                    'confidence': confidence,
                    'all_predictions': {
                        'happy': confidence if dominant == 'POSITIVE' else 0.2,
                        'sad': confidence if dominant == 'NEGATIVE' else 0.2,
                        'neutral': confidence if dominant == 'NEUTRAL' else 0.2,
                        'angry': 0.1,
                        'fear': 0.1,
                        'disgust': 0.1
                    },
                    'transcript': text
                }
            else:
                # Keyword-based fallback
                text_lower = text.lower()
                
                emotion = 'neutral'
                confidence = 0.6
                
                if any(word in text_lower for word in ['happy', 'great', 'amazing', 'wonderful', 'excellent', 'love']):
                    emotion = 'happy'
                    confidence = 0.7
                elif any(word in text_lower for word in ['sad', 'terrible', 'bad', 'awful', 'hate', 'depressed']):
                    emotion = 'sad'
                    confidence = 0.7
                elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'annoyed']):
                    emotion = 'angry'
                    confidence = 0.7
                
                print(f"✓ Keyword-based detection: {emotion} (confidence: {confidence:.2%})")
                
                return {
                    'emotion': emotion,
                    'confidence': confidence,
                    'all_predictions': {emotion: confidence, 'neutral': 0.4},
                    'transcript': text
                }
            
        except aai.exceptions.AuthenticationError:
            print("❌ Authentication failed. Check your API key.")
            print("Get a free API key from: https://www.assemblyai.com/")
            return None
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
