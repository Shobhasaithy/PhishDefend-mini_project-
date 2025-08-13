import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
import logging
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_and_preprocess_data(file_path):
    """Load and preprocess the phishing dataset."""
    logger.info("Loading dataset...")
    df = pd.read_csv(file_path)
    
    # Remove the Index column if it exists
    if 'Index' in df.columns:
        df = df.drop('Index', axis=1)
    
    # Separate features and target
    X = df.drop('class', axis=1)
    y = df['class']
    
    # Convert -1 labels to 0 for binary classification
    y = (y == 1).astype(int)
    
    logger.info(f"Dataset loaded successfully. Shape: {X.shape}")
    return X, y

def create_model_pipeline(X, y):
    """Create an optimized model pipeline with SMOTE and feature selection."""
    # Calculate class weights
    n_samples = len(y)
    n_classes = len(np.unique(y))
    class_weights = dict(zip(
        np.unique(y),
        n_samples / (n_classes * np.bincount(y))
    ))
    
    # Create pipeline steps
    pipeline_steps = [
        ('scaler', StandardScaler()),
        ('smote', SMOTE(random_state=42)),
        ('feature_selector', SelectFromModel(
            RandomForestClassifier(n_estimators=100, random_state=42),
            prefit=False
        )),
        ('classifier', RandomForestClassifier(
            random_state=42,
            class_weight=class_weights,
            n_jobs=-1
        ))
    ]
    
    # Create pipeline
    pipeline = ImbPipeline(pipeline_steps)
    
    # Define parameter grid for GridSearchCV
    param_grid = {
        'classifier__n_estimators': [200, 300, 400],
        'classifier__max_depth': [10, 15, 20],
        'classifier__min_samples_split': [5, 10, 15],
        'classifier__min_samples_leaf': [2, 4, 6],
        'feature_selector__threshold': ['mean', '0.5*mean', '1.5*mean']
    }
    
    return pipeline, param_grid

def evaluate_model(model, X, y):
    """Evaluate model using cross-validation."""
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1')
    logger.info(f"\nCross-validation F1 scores: {cv_scores}")
    logger.info(f"Mean F1 score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

def train_model(X, y):
    """Train the model using GridSearchCV and pipeline."""
    # Create train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    logger.info("Creating model pipeline...")
    pipeline, param_grid = create_model_pipeline(X_train, y_train)
    
    # Perform grid search
    logger.info("Starting GridSearchCV...")
    grid_search = GridSearchCV(
        pipeline,
        param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    
    # Fit the model
    logger.info("Training model with best parameters...")
    grid_search.fit(X_train, y_train)
    
    # Get best model
    best_model = grid_search.best_estimator_
    
    # Log best parameters
    logger.info(f"\nBest parameters found:")
    logger.info(grid_search.best_params_)
    
    # Evaluate model
    logger.info("\nEvaluating model performance...")
    evaluate_model(best_model, X, y)
    
    # Generate predictions and metrics
    y_pred = best_model.predict(X_test)
    
    logger.info("\nClassification Report:")
    logger.info("\n" + classification_report(y_test, y_pred))
    
    logger.info("\nConfusion Matrix:")
    logger.info("\n" + str(confusion_matrix(y_test, y_pred)))
    
    # Get selected features
    feature_selector = best_model.named_steps['feature_selector']
    selected_features = X.columns[feature_selector.get_support()].tolist()
    
    logger.info(f"\nNumber of selected features: {len(selected_features)}")
    logger.info("Selected features:")
    logger.info(selected_features)
    
    return best_model, selected_features

def save_model(model, feature_names):
    """Save the trained model and feature names."""
    try:
        # Save the model
        model_path = 'models/phishing_detector.joblib'
        joblib.dump(model, model_path)
        
        # Save feature names
        feature_path = 'models/feature_names.joblib'
        joblib.dump(feature_names, feature_path)
        
        logger.info(f"Model and feature names saved successfully to {model_path}")
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")
        raise

def main():
    try:
        # Load and preprocess data
        X, y = load_and_preprocess_data('phishing.csv')
        
        # Train model
        model, selected_features = train_model(X, y)
        
        # Save model and feature names
        save_model(model, selected_features)
        
    except Exception as e:
        logger.error(f"Error in training pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
