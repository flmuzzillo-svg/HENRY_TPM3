# Sistema Multi-Agente RAG (Version OpenRouter + Web Interface)

## Descripcion del Proyecto

Esta es la implementación optimizada del ecosistema Multi-Agente RAG. Se caracteriza por su flexibilidad al utilizar **OpenRouter** como puerta de enlace a múltiples LLMs y por reducir drásticamente los costos mediante el uso de **Embeddings locales de HuggingFace**. Además, ofrece una experiencia de usuario completa a través de una interfaz web moderna construida con FastAPI.

## Arquitectura del Sistema

```
[Cliente Web / Consola] 
         |
         v
   [FastAPI Server]
         |
         v
 [Orquestador RAG] --> [HuggingFace Embeddings (Local)] --> [OpenRouter API]
```

## Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| API Provider | OpenRouter |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (Local) |
| Generacion | `gpt-4o` / `claude-3` (vía OpenRouter) |
| Backend | FastAPI |
| Frontend | Vanilla HTML/CSS/JS (Glassmorphism) |
| Vector Store | FAISS |
| Observabilidad | Langfuse |

## Setup — Instalacion

### Paso 1: Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Variables de Entorno
```bash
# Crea un archivo .env con:
OPENROUTER_API_KEY=tu_clave
LANGFUSE_PUBLIC_KEY=tu_clave
LANGFUSE_SECRET_KEY=tu_clave
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Ejecucion

### Opcion A: Consola Interactiva
Inicia el menú interactivo para ejecutar tests o chatear:
```bash
python src/multi_agent_system.py
```

### Opcion B: Interfaz Web
Levanta el servidor para usar el chat en el navegador:
```bash
uvicorn src.app:app --reload
```
Accede en: [http://localhost:8000](http://localhost:8000)

## Diferencias Clave (vs Versión Original)
- **Costo Cero en Embeddings**: Al procesar los vectores localmente con HuggingFace, no hay consumo de cuotas de API por indexación.
- **Interoperabilidad**: Fácil cambio de modelo (GPT, Claude, Llama) sin tocar la lógica central.
- **UX**: Chat con burbujas, estados de carga y etiquetas de dominio.

## Justificacion de la Estrategia
- **HuggingFace Local**: Se seleccionó `all-MiniLM-L6-v2` por su balance entre precisión semántica y bajo consumo de memoria (384 dimensiones).
- **FastAPI**: Elegido por su soporte nativo de asincronía, lo que permite manejar múltiples consultas concurrentes a los agentes RAG sin bloquear el hilo principal.
- **OpenRouter**: Permite evitar el vendor lock-in y optimizar la elección del modelo según la complejidad de la consulta.
