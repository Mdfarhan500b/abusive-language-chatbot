import pandas as pd

# Load both datasets
df1 = pd.read_csv('data/train_data3v2.csv')
df2 = pd.read_csv('data/labeled_data.csv')

# Select relevant columns from both datasets
df1 = df1[['tweet', 'class']]
df2 = df2[['tweet', 'class']]  # Adjust column names if different

# Map 'class' values to numerical labels (1 = Offensive, 0 = Safe)
df1['label'] = df1['class'].map({'Offensive_Speech': 1, 'Safe_Speech': 0})
df2['label'] = df2['class'].map({'Offensive_Speech': 1, 'Safe_Speech': 0})

# Drop the 'class' column as it's no longer needed
df1 = df1[['tweet', 'label']]
df2 = df2[['tweet', 'label']]

# Combine the datasets
combined_df = pd.concat([df1, df2], ignore_index=True)

# Save the combined dataset
combined_df.to_csv('data/processed_train_data.csv', index=False)
print("Data preprocessing complete. Combined data saved as 'data/processed_train_data.csv'.")
