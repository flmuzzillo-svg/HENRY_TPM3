import os
import sys
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler

# Agregar el directorio actual al path para encontrar los agentes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar nuestros agentes modulares
from agents import HRAgent, TechAgent, FinanceAgent, RouterAgent

# Forzar UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

load_dotenv()

app = FastAPI(title="Multi-Agent RAG API")

# Rutas base
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
vs_dir = os.path.join(base_dir, "vector_stores")
static_dir = os.path.join(base_dir, "static")

# Singleton para los agentes
class AgentManager:
    def __init__(self):
        self.agents = None
        self.router = None

    def initialize(self):
        if self.agents is None:
            self.agents = {
                "HR": HRAgent(data_dir=data_dir, vs_dir=vs_dir),
                "IT": TechAgent(data_dir=data_dir, vs_dir=vs_dir),
                "FINANCE": FinanceAgent(data_dir=data_dir, vs_dir=vs_dir)
            }
            self.router = RouterAgent()

manager = AgentManager()

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    manager.initialize()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    langfuse_handler = CallbackHandler()
    query = request.message
    
    try:
        # Enrutar la consulta
        intent = await manager.router.aroute(query, callbacks=[langfuse_handler])
        
        # Procesar con el agente correcto
        if intent in manager.agents:
            response = await manager.agents[intent].aquery(query, callbacks=[langfuse_handler])
            return {
                "intent": intent,
                "response": response,
                "status": "success"
            }
        else:
            return {
                "intent": "UNKNOWN",
                "response": "Lo siento, no puedo ayudarte con esa consulta ya que no pertenece a HR, IT o FINANCE.",
                "status": "no_domain"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir archivos estáticos
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
