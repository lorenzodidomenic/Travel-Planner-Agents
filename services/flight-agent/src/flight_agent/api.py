from fastapi import FastAPI
from pydantic import BaseModel

from flight_agent.agent import agent

app = FastAPI(title="Flight Agent")

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(req: ChatRequest):
    result = await agent.ainvoke({"messages": [{"role": "user", "content": req.message}]})
    return {"reply": result["messages"][-1].content}
