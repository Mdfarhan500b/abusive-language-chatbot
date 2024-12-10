import pandas as pd

# Load the dataset
df = pd.read_csv('data/train_data3v2.csv')

# Select the relevant columns
df = df[['tweet', 'class']]

# Map 'class' values to numerical labels (1 = Offensive, 0 = Safe)
df['label'] = df['class'].map({'Offensive_Speech': 1, 'Safe_Speech': 0})

# Drop the 'class' column as it's no longer needed
df = df[['tweet', 'label']]

# Save the processed dataset
df.to_csv('data/processed_train_data.csv', index=False)
print("Data preprocessing complete. Processed data saved.")
