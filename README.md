# HENRY_TPM3: Multi-Agent RAG Ecosystem

Este repositorio contiene dos implementaciones avanzadas de sistemas Multi-Agente RAG diseñados para entornos corporativos (Recursos Humanos, IT y Finanzas).

## 📁 Proyectos Incluidos

### 1. [Chat_Multi_Agent_RAG_Lang](./Chat_Multi_Agent_RAG_Lang)
Versión base que utiliza el stack nativo de **OpenAI**. Ideal para comparativas y ejecución estándar.
- **Enfoque**: Estabilidad y simplicidad.
- **Stack**: OpenAI + FAISS + LangChain.

### 2. [Chat_Multi_Agent_RAG_Lang_OPENROUTER](./Chat_Multi_Agent_RAG_Lang_OPENROUTER)
Versión extendida y optimizada con mayor flexibilidad.
- **Enfoque**: Reducción de costos (embeddings locales), interoperabilidad (OpenRouter) y experiencia de usuario mejorada.
- **Extras**: Incluye una **Interfaz Web (FastAPI)** y un menú interactivo por consola.

## 🛠️ Cómo empezar
Cada carpeta contiene su propio archivo `requirements.txt` y `README.md` detallado. 

1. Se recomienda usar la versión **OPENROUTER** para la mejor experiencia de usuario.
2. Asegúrate de configurar las variables de entorno en un archivo `.env` dentro de la carpeta del proyecto que desees ejecutar.

---
*Desarrollado como parte del Módulo 3 de Ingeniería en IA.*
