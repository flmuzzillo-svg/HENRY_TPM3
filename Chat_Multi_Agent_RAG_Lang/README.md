# Multi-Agent RAG System (OpenAI Version)

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) avanzado utilizando una arquitectura de múltiples agentes especializados para responder consultas corporativas.

## 🚀 Características
- **Orquestador Inteligente**: Clasifica la intención del usuario y deriva la consulta al agente experto (HR, IT o Finanzas).
- **Agentes Especializados**: Cada agente posee su propio Vector Store basado en documentación específica.
- **Observabilidad con Langfuse**: Trazabilidad completa de las cadenas de pensamiento y llamadas a la API.
- **Evaluación**: Sistema integrado para calificar la calidad de las respuestas.

## 🛠️ Stack Tecnológico
- **LLM**: OpenAI (GPT-4o)
- **Embeddings**: OpenAI Embeddings
- **Framework**: LangChain (LCEL)
- **Vector Store**: FAISS
- **Observabilidad**: Langfuse

## 📋 Requisitos Previos
1. Python 3.9+
2. Claves de API:
   - `OPENAI_API_KEY`
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_HOST`

## ⚙️ Instalación
1. Clonar el repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar el archivo `.env` con tus credenciales.

## 🏃 Ejecución
Para ejecutar las pruebas automáticas y el sistema:
```bash
python src/multi_agent_system.py
```

## 📂 Estructura del Proyecto
- `data/`: Contiene los documentos Markdown con el conocimiento de dominio.
- `src/agents/`: Implementación modular de los agentes y el orquestador.
- `vector_stores/`: Índices FAISS generados automáticamente.
