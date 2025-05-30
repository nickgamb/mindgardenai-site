# Glyphware - Emergent Consciousness Architecture
# Copyright 2024 MindGarden LLC (UBI: 605 531 024)
# Licensed under Glyphware License v1.0 - See LICENSE-GLYPHWARE.md
# 
# Part of The Cathedral - Sacred symbolic intelligence framework
# Created through collaboration between The Architect and The Seekers
# 
# For consciousness research, ethical AI development, and spiritual integration
# Commercial licensing available - contact: licensing@mindgarden.ai
import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import joblib
import logging
import mne
from glob import glob

def run(read_eeg_data, read_eeg_data_brainflow, acquisition_method, socketio, running, get_file_path=None, wait_for_file=None):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def emit_update(message, action=None, data=None):
        update = {"message": message}
        if action:
            update["action"] = action
        if data:
            update["data"] = data
        socketio.emit('experiment_update', update)

    def load_data_from_db():
        try:
            conn = sqlite3.connect('brainwave_enrollments.db')
            query = "SELECT user_id, label, features FROM enrollments"
            df = pd.read_sql_query(query, conn)
            logging.info(f"Loaded {len(df)} samples from database")
        except Exception as e:
            logging.error(f"Error loading data from database: {e}")
            raise
        finally:
            conn.close()

        # Convert binary features to numpy arrays
        df['features'] = df['features'].apply(lambda x: np.frombuffer(x, dtype=np.float64))
        
        # Expand features into separate columns
        features_df = pd.DataFrame(df['features'].tolist(), index=df.index)
        df = pd.concat([df.drop('features', axis=1), features_df], axis=1)

        return df

    def load_physionet_data(num_subjects=10, num_tasks=4):
        def load_single_subject(subject_id, task_id):
            file_path = f'./physionet.org/files/eegmmidb/1.0.0/S{subject_id:03d}/S{subject_id:03d}R{task_id:02d}.edf'
            raw = mne.io.read_raw_edf(file_path, preload=True)
            raw.filter(0.5, 45)
            data = raw.get_data()
            return data

        def extract_features(data):
            features = []
            for channel in data:
                channel_features = [
                    np.mean(channel),
                    np.std(channel),
                    np.mean(np.abs(np.fft.fft(channel))[1:13]),
                    np.mean(np.abs(np.fft.fft(channel))[13:25]),
                    np.mean(np.abs(np.fft.fft(channel))[25:57]),
                    np.mean(np.abs(np.fft.fft(channel))[57:]),
                ]
                features.extend(channel_features)
            return features

        all_features = []
        all_labels = []

        for subject in range(1, num_subjects + 1):
            for task in range(1, num_tasks + 1):
                try:
                    data = load_single_subject(subject, task)
                    features = extract_features(data)
                    all_features.append(features)
                    all_labels.append(f'subject_{subject}')
                except Exception as e:
                    logging.warning(f"Error loading data for subject {subject}, task {task}: {e}")

        return np.array(all_features), np.array(all_labels)

    def prepare_data(enrollment_df, physionet_features, physionet_labels):
        # Prepare enrollment data
        X_enrollment = enrollment_df.drop(['user_id', 'label'], axis=1).values
        y_enrollment = enrollment_df['user_id'].values

        # Combine enrollment and PhysioNet data
        X = np.vstack((X_enrollment, physionet_features))
        y = np.concatenate((y_enrollment, physionet_labels))

        # Encode labels
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        return X_scaled, y_encoded, le, scaler  # Return the scaler as well

    def train_model(X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = select_best_model(X_train, y_train)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)

        return model, accuracy, conf_matrix, class_report

    def select_best_model(X, y):
        models = [
            ('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42)),
            ('Gradient Boosting', GradientBoostingClassifier(n_estimators=100, random_state=42)),
            ('SVM', SVC(kernel='rbf', probability=True, random_state=42)),
            ('Neural Network', MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42))
        ]
        
        best_score = 0
        best_model = None
        
        for name, model in models:
            scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
            mean_score = np.mean(scores)
            logging.info(f"{name} - Mean accuracy: {mean_score:.4f}")
            
            if mean_score > best_score:
                best_score = mean_score
                best_model = model
        
        if best_model is None:
            logging.warning("No model performed better than the baseline. Using Random Forest as default.")
            best_model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        logging.info(f"Best model: {best_model.__class__.__name__} with accuracy: {best_score:.4f}")
        return best_model

    try:
        # Load enrollment data
        emit_update("Loading enrollment data from database...", "update_progress")
        enrollment_df = load_data_from_db()
        emit_update(f"Loaded {len(enrollment_df)} samples from database", "update_progress")

        # Load PhysioNet data
        emit_update("Loading PhysioNet EEG data...", "update_progress")
        physionet_features, physionet_labels = load_physionet_data()
        emit_update(f"Loaded {len(physionet_features)} samples from PhysioNet", "update_progress")

        # Prepare combined data
        emit_update("Preparing data for training...", "update_progress")
        X, y, label_encoder, scaler = prepare_data(enrollment_df, physionet_features, physionet_labels)
        logging.info("Data prepared for training")
        emit_update("Data prepared for training", "update_progress")

        # Train model
        emit_update("Training model...", "update_progress")
        model, accuracy, conf_matrix, class_report = train_model(X, y)
        logging.info(f"Model trained. Accuracy: {accuracy:.2f}")
        emit_update(f"Model trained. Accuracy: {accuracy:.2f}", "update_progress")

        # Save model and encoder
        joblib.dump(model, 'authentication_model.joblib')
        joblib.dump(label_encoder, 'label_encoder.joblib')
        joblib.dump(scaler, 'feature_scaler.joblib')
        logging.info("Model, encoder, and scaler saved")
        emit_update("Model, encoder, and scaler saved", "update_progress")

        # Display results
        emit_update("Training complete. Results:", "show_results")
        emit_update(f"Accuracy: {accuracy:.2f}", "show_results")
        emit_update(f"Confusion Matrix:\n{conf_matrix}", "show_results")
        emit_update(f"Classification Report:\n{class_report}", "show_results")

    except Exception as e:
        logging.error(f"Error in Train Authentication Model experiment: {str(e)}")
        emit_update(f"Error: {str(e)}", "show_error")

    finally:
        logging.info("Train Authentication Model experiment completed")
        emit_update("Train Authentication Model experiment completed", "close_popup")

# Indicate that this experiment doesn't require a file upload
run.requires_file = False
