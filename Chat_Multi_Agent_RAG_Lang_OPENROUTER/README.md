# Multi-Agent RAG System (OpenRouter + Web Interface)

Esta es la versión mejorada y migrada del sistema Multi-Agente RAG, optimizada para el uso de modelos a través de **OpenRouter** y con una **Interfaz Web** moderna.

## ✨ Mejoras y Funcionalidades
- **Independencia de OpenAI**: Utiliza OpenRouter para acceder a una variedad de modelos y **HuggingFace Embeddings** locales para procesar vectores sin costo adicional de API.
- **Interfaz Web Premium**: Chat interactivo con diseño Glassmorphism, animaciones y etiquetas de dominio.
- **Menú de Consola**: Selector interactivo para correr tests automáticos o entrar en modo consultoría.
- **Modernización LCEL**: Implementación total con LangChain Expression Language para mayor robustez.

## 🛠️ Stack Tecnológico
- **LLM**: OpenRouter (GPT-4o / Otros)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`) - *Ejecución Local*
- **Backend**: FastAPI
- **Frontend**: Vanilla JS / CSS (Glassmorphism)
- **Framework**: LangChain (LCEL)
- **Observabilidad**: Langfuse

## 📋 Requisitos Previos
1. Python 3.9+
2. Claves de API:
   - `OPENROUTER_API_KEY`
   - `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`

## ⚙️ Instalación
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar el archivo `.env`.

## 🏃 Cómo usarlo

### Modo Consola (Con Menú)
Ejecuta el sistema principal para acceder a los tests automáticos o al chat por terminal:
```bash
python src/multi_agent_system.py
```

### Modo Web (Interfaz Gráfica)
Inicia el servidor de FastAPI:
```bash
uvicorn src.app:app --reload
```
Luego abre [http://localhost:8000](http://localhost:8000) en tu navegador.

## 📂 Estructura
- `src/app.py`: Servidor web y API.
- `static/`: Interfaz de usuario (HTML/CSS/JS).
- `src/agents/`: Lógica de agentes especializados.
- `data/test_queries.json`: Dataset de pruebas balanceado.
