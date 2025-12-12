import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from torch.utils.data import Dataset, DataLoader
import joblib

# 1. Load Data
print("Loading data...")
try:
    # The file is space-separated with quotes
    df = pd.read_csv("idiopathic_data/GSE173356_PhenoData.txt", sep=" ", quotechar='"')
    print(f"Data loaded: {df.shape}")
except Exception as e:
    print(f"Error loading csv with space sep: {e}")
    # Fallback if separator is different
    try:
        df = pd.read_csv("idiopathic_data/GSE173356_PhenoData.txt", sep="\t", quotechar='"')
        print(f"Data loaded with tab sep: {df.shape}")
    except:
        raise ValueError("Could not read PhenoData file")

# 2. Preprocessing
# Relevant columns based on inspection: 'age:ch1', 'Sex:ch1', 'smoking:ch1', 'diagnosis:ch1'
# We might need to clean column names
df.columns = [c.replace(":ch1", "").lower() for c in df.columns]

target_col = 'diagnosis' # ipf vs normal
feature_cols = ['age', 'sex', 'smoking'] 

print("Columns:", df.columns.tolist())

# Filter for relevant rows/cols
data = df[feature_cols + [target_col]].copy()
data.dropna(inplace=True)

# Clean strings
data['sex'] = data['sex'].astype(str).str.strip().str.lower()
data['smoking'] = data['smoking'].astype(str).str.strip().str.title()
data['diagnosis'] = data['diagnosis'].astype(str).str.strip().str.lower()

print("Sex values:", data['sex'].unique())
print("Smoking values:", data['smoking'].unique())
print("Diagnosis values:", data['diagnosis'].unique())

# Encoding
le_sex = LabelEncoder()
data['sex'] = le_sex.fit_transform(data['sex'])

le_smoke = LabelEncoder()
data['smoking'] = le_smoke.fit_transform(data['smoking'])

le_target = LabelEncoder()
data['target'] = le_target.fit_transform(data['diagnosis'])


print("Classes:", le_target.classes_)
# We want prediction of IPF. Let's ensure IPF is 1 if possible, or just track the classes.
# If classes are ['ipf', 'normal'], then ipf=0, normal=1. 
# Let's verify mapping.
ipf_code = le_target.transform(['ipf'])[0]
print(f"IPF Code: {ipf_code}")

X = data[['age', 'sex', 'smoking']].values
y = data['target'].values

# Scale Age
scaler = StandardScaler()
X[:, 0] = scaler.fit_transform(X[:, 0].reshape(-1, 1)).flatten()

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to Tensors
X_train_t = torch.FloatTensor(X_train)
y_train_t = torch.FloatTensor(y_train).reshape(-1, 1)
X_test_t = torch.FloatTensor(X_test)
y_test_t = torch.FloatTensor(y_test).reshape(-1, 1)

# 3. Model Definition
class IdiopathicNN(nn.Module):
    def __init__(self, input_dim):
        super(IdiopathicNN, self).__init__()
        self.layer1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(16, 8)
        self.output = nn.Linear(8, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.sigmoid(self.output(x))
        return x

model = IdiopathicNN(input_dim=3)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 4. Training
print("Training model...")
epochs = 100
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# 5. Evaluation
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_t)
    predicted = (test_outputs > 0.5).float()
    accuracy = (predicted == y_test_t).float().mean()
    print(f"Test Accuracy: {accuracy.item():.4f}")

# 6. Save Artifacts
print("Saving artifacts...")
torch.save(model.state_dict(), "idiopathic_model.pth")
joblib.dump(scaler, "idiopathic_scaler.pkl")
joblib.dump({'sex': le_sex, 'smoking': le_smoke, 'target': le_target}, "idiopathic_encoders.pkl")
print("Done.")
