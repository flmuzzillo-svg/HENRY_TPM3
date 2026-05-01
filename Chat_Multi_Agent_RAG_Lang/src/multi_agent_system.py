import os
import sys
import asyncio

# Forzar UTF-8 en la salida para evitar UnicodeEncodeError en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from dotenv import load_dotenv
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse

# Importar nuestros agentes modulares
from agents import HRAgent, TechAgent, FinanceAgent, RouterAgent

# Configuración de Entorno
load_dotenv()

# Instanciar el cliente de Langfuse para evaluaciones
langfuse = Langfuse()

def evaluate_response(trace_id: str, score: float, comment: str = ""):
    """
    Evalúa una respuesta asignando un score de 1 a 10 usando Langfuse.
    """
    print(f"[Evaluación] Registrando score {score}/10 para el trace {trace_id}")
    try:
        # Langfuse v3/v4 usa create_score()
        langfuse.create_score(
            trace_id=trace_id,
            name="user-helpfulness",
            value=score,
            comment=comment
        )
    except AttributeError:
        # Fallback para versiones antiguas
        langfuse.score(
            trace_id=trace_id,
            name="user-helpfulness",
            value=score,
            comment=comment
        )

async def main():
    # Inicializar Langfuse CallbackHandler para trace
    langfuse_handler = CallbackHandler()
    
    # Rutas base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    vs_dir = os.path.join(base_dir, "vector_stores")
    
    # Inicializar Agentes RAG (esto bloquea la primera vez mientras genera índices, luego es instantáneo)
    agents = {
        "HR": HRAgent(data_dir=data_dir, vs_dir=vs_dir),
        "IT": TechAgent(data_dir=data_dir, vs_dir=vs_dir),
        "FINANCE": FinanceAgent(data_dir=data_dir, vs_dir=vs_dir)
    }
    
    router = RouterAgent()
    
    import json
    
    # Cargar consultas de prueba
    test_queries_path = os.path.join(data_dir, "test_queries.json")
    with open(test_queries_path, "r", encoding="utf-8") as f:
        test_queries = json.load(f)
    
    for query_info in test_queries:
        query = query_info["query"]
        expected = query_info["expected_domain"]
        print(f"\n--- Consulta ({expected}): '{query}' ---")
        
        # Enrutar la consulta
        intent = await router.aroute(query, callbacks=[langfuse_handler])
        print(f"[Router] Intención detectada: {intent}")
        
        # Procesar con el agente correcto
        if intent in agents:
            response = await agents[intent].aquery(query, callbacks=[langfuse_handler])
            safe_response = response.encode('utf-8', errors='replace').decode('utf-8')
            print(f"[Respuesta] {safe_response}")
            
            # Bonus: Evaluar (ejemplo hardcodeado de score 9/10 para ilustrar)
            # Extraemos el trace_id del handler actual
            trace_id = getattr(langfuse_handler, "last_trace_id", None) or getattr(langfuse_handler, "get_trace_id", lambda: None)()
            if trace_id:
                evaluate_response(trace_id=trace_id, score=9.0, comment="Respuesta evaluada automáticamente.")
        else:
            print("[Respuesta] Lo siento, no puedo ayudarte con esa consulta ya que no pertenece a HR, IT o FINANCE.")
        
    # Flush langfuse al final (compatible con v2/v3/v4)
    if hasattr(langfuse_handler, 'flush'):
        langfuse_handler.flush()
    langfuse.flush()

if __name__ == "__main__":
    asyncio.run(main())
