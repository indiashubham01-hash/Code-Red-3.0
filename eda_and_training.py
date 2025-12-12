import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import os

import joblib
from model_utils import CardioNN

# Set random seed for reproducibility
np.random.seed(42)
torch.manual_seed(42)

# 1. Load Data
# ... (rest of loading code same)
print("Loading data...")
try:
    df = pd.read_csv('cardio_train.csv', sep=';')
except FileNotFoundError:
    print("Error: cardio_train.csv not found.")
    exit()

print(f"Dataset shape: {df.shape}")
print(df.head())

# 2. EDA & Cleaning
print("\nPerforming EDA and Cleaning...")

# Check for duplicates
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")
if duplicates > 0:
    df.drop_duplicates(inplace=True)
    print("Duplicates dropped.")

# Basic stats
print(df.describe())

# Convert age from days to years
df['age_years'] = df['age'] / 365.25

# Visualizations
if not os.path.exists('plots'):
    os.makedirs('plots')

# Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Matrix')
plt.savefig('plots/correlation_matrix.png')
plt.close()

# Distribution of Age
plt.figure(figsize=(10, 6))
sns.histplot(df['age_years'], bins=30, kde=True)
plt.title('Age Distribution')
plt.savefig('plots/age_distribution.png')
plt.close()

# Outlier Removal (Simple logic for BP and Height/Weight)
# Removing impossible blood pressures
# ap_hi should be > ap_lo
# Reasonable ranges: ap_hi [60, 240], ap_lo [30, 160]
print("Removing outliers...")
initial_shape = df.shape
df = df[(df['ap_hi'] >= 60) & (df['ap_hi'] <= 240) & 
        (df['ap_lo'] >= 30) & (df['ap_lo'] <= 160) & 
        (df['ap_hi'] > df['ap_lo'])]

# Height and Weight reasonable ranges
df = df[(df['height'] >= 100) & (df['height'] <= 250)]
df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]

print(f"Shape after outlier removal: {df.shape} (Removed {initial_shape[0] - df.shape[0]} rows)")

# 3. Preprocessing
# Drop 'id' and 'age' (using age_years might be better, or just scale age)
# Let's use 'age' (days) or 'age_years'. 'age' is fine if scaled.
X = df.drop(['cardio', 'id', 'age_years'], axis=1) # Keep original age column, it's fine
# Or use age_years and drop age. Let's use age_years as it acts same but easier to read.
X = df.drop(['cardio', 'id', 'age'], axis=1)
y = df['cardio']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the scaler
joblib.dump(scaler, 'scaler.pkl')
print("Scaler saved to scaler.pkl")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train.values).reshape(-1, 1)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test.values).reshape(-1, 1)

# Create DataLoaders
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 4. Model Definition
# CardioNN is now imported from model_utils

model = CardioNN(X_train.shape[1])
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 5. Training
print("\nStarting training...")
epochs = 50
best_acc = 0.0
best_model_path = "cardio_model.pth"

train_losses = []
val_accuracies = []

for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    
    avg_loss = running_loss / len(train_loader)
    train_losses.append(avg_loss)
    
    # Validation
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            predicted = (torch.sigmoid(outputs) > 0.5).float()
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = correct / total
    val_accuracies.append(accuracy)
    
    if accuracy > best_acc:
        best_acc = accuracy
        torch.save(model.state_dict(), best_model_path)
    
    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.4f}")

# Plot Training History
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Training Loss')
plt.title('Training Loss')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(val_accuracies, label='Validation Accuracy', color='orange')
plt.title('Validation Accuracy')
plt.legend()
plt.savefig('plots/training_history.png')
plt.close()

print(f"\nTraining complete. Best Validation Accuracy: {best_acc:.4f}")
print(f"Model saved to {best_model_path}")

# 6. Final Evaluation
model.load_state_dict(torch.load(best_model_path)) # Load best model
model.eval()
all_preds = []
all_labels = []
with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        predicted = (torch.sigmoid(outputs) > 0.5).float()
        all_preds.extend(predicted.numpy())
        all_labels.extend(labels.numpy())

print("\nFinal Classification Report:")
print(classification_report(all_labels, all_preds))
