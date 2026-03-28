import numpy as np
import librosa
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import pickle
import matplotlib.pyplot as plt

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, 'datasets', 'audio_emotions')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'voice_emotion', 'ml_models', 'voice_emotion_model.h5')
ENCODER_SAVE_PATH = os.path.join(BASE_DIR, 'voice_emotion', 'ml_models', 'label_encoder.pkl')
SCALER_SAVE_PATH = os.path.join(BASE_DIR, 'voice_emotion', 'ml_models', 'scaler.pkl')

# Ensure directories exist
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

print("=" * 50)
print("VOICE EMOTION RECOGNITION TRAINING")
print("=" * 50)

# Extract enhanced features from audio
def extract_enhanced_features(file_path, duration=3):
    try:
        audio, sample_rate = librosa.load(file_path, duration=duration, sr=22050)
        
        if len(audio) < 1024:
            return None
        
        # Use adaptive n_fft
        n_fft = min(2048, len(audio))
        hop_length = n_fft // 4
        
        # MFCC features (40 coefficients)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40, n_fft=n_fft, hop_length=hop_length)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        mfccs_std = np.std(mfccs.T, axis=0)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)
        chroma_mean = np.mean(chroma.T, axis=0)
        chroma_std = np.std(chroma.T, axis=0)
        
        # Mel-spectrogram
        mel = librosa.feature.melspectrogram(y=audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)
        mel_mean = np.mean(mel.T, axis=0)
        mel_std = np.std(mel.T, axis=0)
        
        # Spectral contrast
        contrast = librosa.feature.spectral_contrast(y=audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)
        contrast_mean = np.mean(contrast.T, axis=0)
        contrast_std = np.std(contrast.T, axis=0)
        
        # Tonnetz
        harmonic = librosa.effects.harmonic(audio)
        tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sample_rate)
        tonnetz_mean = np.mean(tonnetz.T, axis=0)
        tonnetz_std = np.std(tonnetz.T, axis=0)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio)
        zcr_mean = np.mean(zcr)
        zcr_std = np.std(zcr)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)[0]
        
        # RMS Energy
        rms = librosa.feature.rms(y=audio)[0]
        rms_mean = np.mean(rms)
        rms_std = np.std(rms)
        
        # Concatenate all features
        features = np.concatenate([
            mfccs_mean, mfccs_std,
            chroma_mean, chroma_std,
            mel_mean, mel_std,
            contrast_mean, contrast_std,
            tonnetz_mean, tonnetz_std,
            [zcr_mean, zcr_std],
            [np.mean(spectral_centroids), np.std(spectral_centroids)],
            [np.mean(spectral_rolloff), np.std(spectral_rolloff)],
            [rms_mean, rms_std]
        ])
        
        return features
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Load data
def load_audio_emotion_data():
    emotions = []
    features = []
    
    for emotion_folder in os.listdir(DATASET_PATH):
        emotion_path = os.path.join(DATASET_PATH, emotion_folder)
        if not os.path.isdir(emotion_path):
            continue
        
        file_count = 0
        for file in os.listdir(emotion_path):
            if file.endswith('.wav'):
                file_path = os.path.join(emotion_path, file)
                feature = extract_enhanced_features(file_path)
                if feature is not None:
                    features.append(feature)
                    emotions.append(emotion_folder)
                    file_count += 1
                    
                    if len(features) % 100 == 0:
                        print(f"Processed {len(features)} files...")
        
        print(f"Loaded {file_count} files from {emotion_folder}")
    
    return np.array(features), np.array(emotions)

print("Loading and processing audio data...")
X, y = load_audio_emotion_data()

print(f"\nTotal samples: {len(X)}")
print(f"Feature shape: {X.shape}")
print(f"Emotion distribution:")
unique, counts = np.unique(y, return_counts=True)
for emotion, count in zip(unique, counts):
    print(f"  {emotion}: {count}")

if len(X) == 0:
    raise RuntimeError("No audio data found! Ensure folders contain .wav files.")

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = keras.utils.to_categorical(y_encoded)

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save encoder and scaler
with open(ENCODER_SAVE_PATH, 'wb') as f:
    pickle.dump(label_encoder, f)
with open(SCALER_SAVE_PATH, 'wb') as f:
    pickle.dump(scaler, f)

print(f"\n✓ Label encoder saved to {ENCODER_SAVE_PATH}")
print(f"✓ Scaler saved to {SCALER_SAVE_PATH}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_categorical, test_size=0.2, random_state=42, stratify=y_encoded
)

# Reshape for LSTM
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

print(f"\nTraining shape: {X_train.shape}")
print(f"Testing shape: {X_test.shape}")

# Build improved model with LSTM and CNN
def create_improved_voice_model(input_shape, num_classes):
    inputs = layers.Input(shape=input_shape)
    
    # CNN blocks
    x = layers.Conv1D(128, 5, padding='same', activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    
    x = layers.Conv1D(256, 5, padding='same', activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling1D(2)(x)
    x = layers.Dropout(0.3)(x)
    
    # LSTM layers
    x = layers.LSTM(128, return_sequences=True)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.LSTM(64)(x)
    x = layers.Dropout(0.3)(x)
    
    # Dense layers
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.4)(x)
    
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    return model

# Create and compile
model = create_improved_voice_model(
    input_shape=(X_train.shape[1], 1),
    num_classes=len(label_encoder.classes_)
)

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
)

print("\n" + model.summary())

# Train
print("\n" + "=" * 50)
print("STARTING TRAINING")
print("=" * 50)

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=32,
    callbacks=[
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=7, min_lr=1e-7, verbose=1),
        ModelCheckpoint(MODEL_SAVE_PATH, save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)
    ],
    verbose=1
)

# Evaluate
test_loss, test_accuracy, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=1)
test_f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall + 1e-7)

print(f"\nTest Results:")
print(f"  Accuracy: {test_accuracy*100:.2f}%")
print(f"  Precision: {test_precision*100:.2f}%")
print(f"  Recall: {test_recall*100:.2f}%")
print(f"  F1-Score: {test_f1*100:.2f}%")

model.save(MODEL_SAVE_PATH)
print(f"\n✓ Model saved to {MODEL_SAVE_PATH}")

# Plot
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title('Accuracy')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title('Loss')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'voice_emotion', 'ml_models', 'training_history.png'))
print("✓ Training plots saved")

print("\n" + "=" * 50)
print("TRAINING COMPLETED!")
print("=" * 50)
