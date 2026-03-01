import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import mlflow.pyfunc

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, confusion_matrix

# Set MLflow experiment
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Flipkart_Sentiment_Experiment_Tracking_and_Model_Management_with_MLflow")

def train_model(C_value=1.0):

    with mlflow.start_run(run_name=f"LogReg_C_{C_value}"):

        # Load dataset
        df = pd.read_csv("reviews_badminton/data.csv")  # change path if needed

        df = df[['Review text', 'Ratings']]
        df.dropna(inplace=True)

        # Create sentiment label
        df['sentiment'] = df['Ratings'].apply(lambda x: 1 if x >= 3 else 0)

        X = df['Review text']
        y = df['sentiment']

        # TF-IDF
        vectorizer = TfidfVectorizer(max_features=5000)
        X = vectorizer.fit_transform(X)

        # Train test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Model
        model = LogisticRegression(C=C_value, max_iter=1000)
        model.fit(X_train, y_train)

        # Prediction
        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred)

        # -------- MLflow Logging --------
        mlflow.log_param("C", C_value)
        mlflow.log_param("max_features", 5000)

        mlflow.log_metric("f1_score", f1)

        # Confusion matrix plot
        cm = confusion_matrix(y_test, y_pred)
        plt.figure()
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title("Confusion Matrix")
        plt.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")

        # Log and register model
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="Flipkart_Sentiment_Model"
        )

        # Add tags
        mlflow.set_tag("project", "Flipkart Sentiment")
        mlflow.set_tag("algorithm", "Logistic Regression")

        print("F1 Score:", f1)


if __name__ == "__main__":
    for C in [0.1, 1.0, 10.0]:
        train_model(C)