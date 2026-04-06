import torch
import torch.nn as nn
import re
import os

# 1. Architecture (Exact copy from training)
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, extra_feat_dim):
        super(LSTMClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.extra_fc = nn.Linear(extra_feat_dim, 32)
        self.fc = nn.Linear(hidden_dim*2 + 32, 1)
        self.dropout = nn.Dropout(0.3)

    def forward(self, text, extra):
        embedded = self.embedding(text)
        _, (hidden, _) = self.lstm(embedded)
        text_features = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1))
        extra_features = torch.relu(self.extra_fc(extra))
        combined = torch.cat((text_features, extra_features), dim=1)
        return self.fc(combined)

# --- LOAD PROCESS ---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "job_classifier_v1.pth")

# Load checkpoint
checkpoint = torch.load(MODEL_PATH, weights_only=False, map_location="cpu")

# Extract metadata
vocab = checkpoint["vocab"]
THRESHOLD = checkpoint["threshold"]

# !!! THE MISSING INITIALIZATION STEPS !!!
model = LSTMClassifier(
    vocab_size=len(vocab),
    embed_dim=128,
    hidden_dim=128,
    extra_feat_dim=3 
)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval() 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

print("✅ Model loaded and ready for inference")
print(f"Loaded threshold: {THRESHOLD}")

# --- PREDICTION LOGIC ---

def tokenize(text):
    return re.sub(r'\W+', ' ', text.lower()).split()

def predict(text, extra_features):
    # 1. Encode text
    encoded = [vocab.get(word, vocab.get("<UNK>", 1)) for word in tokenize(text)]
    text_tensor = torch.tensor([encoded])
    
    # 2. Extra features
    extra_tensor = torch.tensor([extra_features], dtype=torch.float32)

    # 3. Forward pass
    with torch.no_grad():
        output = model(text_tensor, extra_tensor)
        prob_fake = torch.sigmoid(output).item()
        prob_real = 1 - prob_fake
        pred_class = int(prob_fake >= THRESHOLD)

    label_map = {0: "Real Job Posting", 1: "Fake Job Posting"}
    
    if pred_class == 1:
        risk = "⚠️ High risk of fake posting"
    elif prob_fake > 0.5:
        risk = "ℹ️ Some caution advised"
    else:
        risk = "✅ Low risk of fake posting"

    return {
        "prediction": pred_class,
        "label": label_map[pred_class],
        "prob_real": round(prob_real * 100, 2),
        "prob_fake": round(prob_fake * 100, 2),
        "probability": round(prob_fake * 100, 2), 
        "risk": risk
    }
