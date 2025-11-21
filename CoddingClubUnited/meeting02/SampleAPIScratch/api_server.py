import torch
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load model and tokenizer
from train_tiny_gpt import TinyGPT, ByteTokenizer, args

tokenizer = ByteTokenizer()

model = TinyGPT(
    vocab_size=args.vocab_size,
    n_embd=args.n_embd,
    n_layer=args.n_layer,
    n_head=args.n_head,
    context=args.context,
    dropout=args.dropout
)

model.load_state_dict(torch.load("checkpoints/best.pt", map_location=args.device))
model.to(args.device)
model.eval()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    history: list
    message: str

def build_chat_prompt(history, user_msg):
    prompt = ""
    for turn in history:
        prompt += f"User: {turn['user']}\nAssistant: {turn['bot']}\n"
    prompt += f"User: {user_msg}\nAssistant:"
    return prompt

@app.post("/chat")
async def chat(req: ChatRequest):
    prompt = build_chat_prompt(req.history, req.message)

    ids = tokenizer.encode(prompt)
    x = torch.tensor([ids], dtype=torch.long).to(args.device)

    with torch.no_grad():
        out = model.generate(
            x, max_new_tokens=120, temperature=0.8, top_k=50
        )

    reply_tokens = out[0].tolist()[len(ids):]
    reply = tokenizer.decode(reply_tokens)

    return {"response": reply}
