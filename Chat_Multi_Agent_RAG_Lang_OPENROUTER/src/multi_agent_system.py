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

async def run_automated_tests(agents, router, test_queries, langfuse_handler):
    """Ejecuta la batería de pruebas automáticas."""
    print("\n" + "="*50)
    print(" INICIANDO BATERÍA DE PRUEBAS AUTOMÁTICAS")
    print("="*50)
    
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
            
            # Extraemos el trace_id del handler actual
            trace_id = getattr(langfuse_handler, "last_trace_id", None) or getattr(langfuse_handler, "get_trace_id", lambda: None)()
            if trace_id:
                evaluate_response(trace_id=trace_id, score=9.0, comment="Prueba automática.")
        else:
            print("[Respuesta] Lo siento, no puedo ayudarte con esa consulta ya que no pertenece a HR, IT o FINANCE.")

async def interactive_mode(agents, router, langfuse_handler):
    """Permite al usuario ingresar consultas manualmente."""
    print("\n" + "="*50)
    print(" MODO INTERACTIVO HABILITADO")
    print(" Escribe 'salir' para terminar")
    print("="*50)
    
    while True:
        try:
            # En Windows, input() puede tener problemas con UTF-8, pero el wrapper de sys.stdout ayuda
            query = input("\nPregunta: ").strip()
            
            if query.lower() in ["salir", "exit", "quit"]:
                break
            
            if not query:
                continue
                
            # Enrutar la consulta
            intent = await router.aroute(query, callbacks=[langfuse_handler])
            print(f"[Router] Intención detectada: {intent}")
            
            # Procesar con el agente correcto
            if intent in agents:
                response = await agents[intent].aquery(query, callbacks=[langfuse_handler])
                safe_response = response.encode('utf-8', errors='replace').decode('utf-8')
                print(f"[Respuesta] {safe_response}")
            else:
                print("[Respuesta] Lo siento, no puedo ayudarte con esa consulta ya que no pertenece a HR, IT o FINANCE.")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[Error] {e}")

async def main():
    # Inicializar Langfuse CallbackHandler para trace
    langfuse_handler = CallbackHandler()
    
    # Rutas base
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    vs_dir = os.path.join(base_dir, "vector_stores")
    
    # Inicializar Agentes RAG
    agents = {
        "HR": HRAgent(data_dir=data_dir, vs_dir=vs_dir),
        "IT": TechAgent(data_dir=data_dir, vs_dir=vs_dir),
        "FINANCE": FinanceAgent(data_dir=data_dir, vs_dir=vs_dir)
    }
    
    router = RouterAgent()
    
    import json
    
    # Cargar consultas de prueba
    test_queries_path = os.path.join(data_dir, "test_queries.json")
    test_queries = []
    if os.path.exists(test_queries_path):
        with open(test_queries_path, "r", encoding="utf-8") as f:
            test_queries = json.load(f)
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA MULTI-AGENTE RAG - MENÚ PRINCIPAL")
        print("="*50)
        print("1. Ejecutar batería de pruebas automáticas (Test)")
        print("2. Iniciar consultoría interactiva (Chat)")
        print("3. SALIR")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            await run_automated_tests(agents, router, test_queries, langfuse_handler)
        elif opcion == "2":
            await interactive_mode(agents, router, langfuse_handler)
        elif opcion == "3" or opcion.lower() == "salir":
            print("Saliendo del sistema...")
            break
        else:
            print("[!] Opción no válida. Por favor, intente de nuevo.")
        
    # Flush langfuse al final
    if hasattr(langfuse_handler, 'flush'):
        langfuse_handler.flush()
    langfuse.flush()

if __name__ == "__main__":
    asyncio.run(main())
