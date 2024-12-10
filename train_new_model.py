import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

# Step 1: Load the preprocessed data
data = pd.read_csv('data/processed_train_data.csv')  # Ensure this file exists in your 'data' folder

# Step 2: Prepare the features (X) and target (y)
X = data['tweet']  # This is the column with the text
y = data['label']  # Correct target column

# Step 3: Handle NaN values in y
y = y.dropna()  # Drop any rows with NaN in the target column
X = X[y.index]  # Ensure X aligns with the cleaned y

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer(max_features=10000)  # This converts the text data into numerical format

# Step 6: Fit and transform the training data
X_train_tfidf = vectorizer.fit_transform(X_train)

# Step 7: Train the model using Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

# Step 8: Evaluate the model on the test data
X_test_tfidf = vectorizer.transform(X_test)  # Transform the test data
y_pred = model.predict(X_test_tfidf)  # Make predictions

# Print the performance of the model
print(classification_report(y_test, y_pred))

# Step 9: Save the trained model and vectorizer to files
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)  # Save the model

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)  # Save the vectorizer

print("Model training complete and saved.")
