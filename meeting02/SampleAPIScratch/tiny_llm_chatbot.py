"""
=======================================================
 TINY LLM CHATBOT — ALL IN ONE PYTHON FILE
 - Tiny GPT from scratch
 - Self-contained toy chat dataset
 - Training loop
 - Chat generation
 - FastAPI REST API server
=======================================================
"""

import torch
import torch.nn as nn
from torch.nn import functional as F
import math, random, argparse, json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# ---------------------------
# 1. CONFIG
# ---------------------------
class Config:
    vocab_size = 256
    context = 128
    n_layer = 4
    n_head = 4
    n_embd = 256
    dropout = 0.1
    batch_size = 16
    lr = 3e-4
    epochs = 4
    device = "cuda" if torch.cuda.is_available() else "cpu"

cfg = Config()

# ---------------------------
# 2. BYTE TOKENIZER
# ---------------------------
class ByteTokenizer:
    def encode(self, text: str):
        return list(text.encode("utf-8"))

    def decode(self, tokens):
        return bytes(tokens).decode("utf-8", errors="replace")

tokenizer = ByteTokenizer()

# ---------------------------
# 3. TINY GPT MODEL
# ---------------------------
class CausalSelfAttention(nn.Module):
    def __init__(self):
        super().__init__()
        assert cfg.n_embd % cfg.n_head == 0
        self.head_dim = cfg.n_embd // cfg.n_head
        self.qkv = nn.Linear(cfg.n_embd, 3 * cfg.n_embd)
        self.proj = nn.Linear(cfg.n_embd, cfg.n_embd)
        self.dropout = nn.Dropout(cfg.dropout)
        self.register_buffer("mask", torch.tril(torch.ones(cfg.context, cfg.context)))

    def forward(self, x):
        B, T, C = x.size()
        qkv = self.qkv(x).view(B, T, 3, cfg.n_head, self.head_dim)
        q, k, v = qkv.unbind(2)

        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(self.mask[:T, :T] == 0, -1e10)
        att = F.softmax(att, dim=-1)
        out = att @ v
        out = out.transpose(1, 2).contiguous().view(B, T, C)
        return self.dropout(self.proj(out))

class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.attn = CausalSelfAttention()
        self.ff = nn.Sequential(
            nn.Linear(cfg.n_embd, 4 * cfg.n_embd),
            nn.GELU(),
            nn.Linear(4 * cfg.n_embd, cfg.n_embd),
            nn.Dropout(cfg.dropout)
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.ff(self.ln2(x))

class TinyGPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(cfg.vocab_size, cfg.n_embd)
        self.pos = nn.Embedding(cfg.context, cfg.n_embd)
        self.blocks = nn.Sequential(*[Block() for _ in range(cfg.n_layer)])
        self.ln_f = nn.LayerNorm(cfg.n_embd)
        self.head = nn.Linear(cfg.n_embd, cfg.vocab_size)

    def forward(self, idx):
        B, T = idx.size()
        x = self.tok(idx) + self.pos(torch.arange(T, device=idx.device))
        x = self.blocks(x)
        x = self.ln_f(x)
        return self.head(x)

    @torch.no_grad()
    def generate(self, idx, max_new=80, temp=0.9, top_k=40):
        for _ in range(max_new):
            inp = idx[:, -cfg.context:]
            logits = self(inp)[:, -1, :] / temp
            if top_k:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -1e10
            probs = F.softmax(logits, dim=-1)
            nxt = torch.multinomial(probs, 1)
            idx = torch.cat([idx, nxt], dim=1)
        return idx

model = TinyGPT().to(cfg.device)

# ---------------------------
# 4. CHAT FORMATTING
# ---------------------------
def build_prompt(history, msg):
    prompt = ""
    for turn in history:
        prompt += f"User: {turn['user']}\nAssistant: {turn['bot']}\n"
    prompt += f"User: {msg}\nAssistant:"
    return prompt

# ---------------------------
# 5. TRAINING DATA (INSIDE FILE)
# ---------------------------
chat_data = [
    ("Hello", "Hi! How can I assist you?"),
    ("What is AI?", "AI means Artificial Intelligence."),
    ("Tell me a joke", "Why did the robot learn coding? To debug its life!"),
    ("What is robotics?", "Robotics is the science of building intelligent machines."),
]

def make_training_text():
    lines = []
    for a, b in chat_data:
        lines.append(f"User: {a}\nAssistant: {b}\n")
    return "".join(lines)

# ---------------------------
# 6. TRAINING LOOP
# ---------------------------
def train():
    print("=== TRAINING START ===")
    text = make_training_text()
    data = tokenizer.encode(text)
    data = torch.tensor(data, dtype=torch.long)

    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg.lr)
    loss_fn = nn.CrossEntropyLoss()

    for epoch in range(cfg.epochs):
        losses = []
        for _ in range(200):  # small training steps
            i = random.randint(0, max(0, len(data) - cfg.context - 1))
            x = data[i:i+cfg.context]
            y = data[i+1:i+1+cfg.context]
            x = x.unsqueeze(0).to(cfg.device)
            y = y.unsqueeze(0).to(cfg.device)

            logits = model(x)
            loss = loss_fn(logits.view(-1, cfg.vocab_size), y.view(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            losses.append(loss.item())

        print(f"Epoch {epoch+1}/{cfg.epochs} | Loss={sum(losses)/len(losses):.4f}")

    torch.save(model.state_dict(), "tiny_llm.pt")
    print("Model saved as tiny_llm.pt")

# ---------------------------
# 7. CHATBOT LOOP
# ---------------------------
def chat():
    print("=== Chatbot Ready ===")
    history = []

    while True:
        msg = input("You: ")
        prompt = build_prompt(history, msg)
        ids = tokenizer.encode(prompt)
        x = torch.tensor([ids]).to(cfg.device)

        out = model.generate(x)
        reply = tokenizer.decode(out[0].tolist()[len(ids):])
        print("Bot:", reply)

        history.append({"user": msg, "bot": reply})

# ---------------------------
# 8. API SERVER
# ---------------------------
app = FastAPI()

class Request(BaseModel):
    history: list
    message: str

@app.post("/chat")
def api_chat(req: Request):
    prompt = build_prompt(req.history, req.message)
    ids = tokenizer.encode(prompt)
    x = torch.tensor([ids]).to(cfg.device)
    out = model.generate(x)
    reply = tokenizer.decode(out[0].tolist()[len(ids):])
    return {"response": reply}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ---------------------------
# 9. MAIN ENTRY
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--chat", action="store_true")
    parser.add_argument("--api", action="store_true")
    args = parser.parse_args()

    if args.train:
        train()
    elif args.chat:
        model.load_state_dict(torch.load("tiny_llm.pt", map_location=cfg.device))
        chat()
    elif args.api:
        model.load_state_dict(torch.load("tiny_llm.pt", map_location=cfg.device))
        run_api()
    else:
        print("Use --train or --chat or --api")
