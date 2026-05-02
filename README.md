# HENRY_TPM3: Ecosistema Multi-Agente RAG

## Descripcion del Proyecto

Este repositorio contiene un ecosistema de dos sistemas RAG (Retrieval-Augmented Generation) diseñados con una arquitectura de **Múltiples Agentes Especializados**. El sistema es capaz de orquestar consultas corporativas y dirigirlas a departamentos específicos de **Recursos Humanos**, **Tecnología** o **Finanzas**, utilizando agentes expertos que consultan su propia base de conocimientos.

Se incluyen dos versiones principales para comparar estrategias de despliegue, costos y flexibilidad.

## Arquitectura del Ecosistema

```
      Pregunta del Usuario
               |
               v
      [Orquestador Experto] -- Clasifica intención --> {HR, IT, FINANCE, UNKNOWN}
               |
               v
     [Agente Especialista] -- Recupera contexto (FAISS) --> Genera Respuesta (LLM)
               |
               v
      [Langfuse Tracing] -- Registro de trazas y evaluación de calidad
```

## Comparativa de Versiones

| Aspecto | Chat_Multi_Agent_RAG_Lang | Chat_Multi_Agent_RAG_Lang_OPENROUTER |
|---|---|---|
| **Proveedor LLM** | OpenAI (Directo) | OpenRouter (Multi-modelo) |
| **Embeddings** | OpenAI (vía API) | HuggingFace (Local / `all-MiniLM-L6-v2`) |
| **Costo** | Basado en tokens (LLM + Embeddings) | Reducido (Embeddings gratis/locales) |
| **Interfaz** | Consola (Automática) | Consola (Menú) + Interfaz Web (FastAPI) |
| **Observabilidad** | Langfuse | Langfuse |

## Estructura del Repositorio

- **[Chat_Multi_Agent_RAG_Lang](./Chat_Multi_Agent_RAG_Lang)**: Versión original optimizada para el stack nativo de OpenAI.
- **[Chat_Multi_Agent_RAG_Lang_OPENROUTER](./Chat_Multi_Agent_RAG_Lang_OPENROUTER)**: Versión extendida con embeddings locales, soporte multi-proveedor y chat web.

## Justificacion de la Estrategia de Chunking

En ambos proyectos se utiliza `RecursiveCharacterTextSplitter` con la siguiente configuración:
- **chunk_size = 1000**: Permite capturar bloques completos de políticas o procedimientos técnicos sin fragmentar demasiado la información.
- **chunk_overlap = 100**: Garantiza la continuidad semántica entre fragmentos adyacentes, evitando la pérdida de contexto en los puntos de corte.
- **Estrategia**: Se priorizan los saltos de línea dobles (`\n\n`) para respetar la estructura de párrafos de los documentos Markdown originales.

## Métricas de Calidad
- **Cobertura**: El sistema indexa el 100% de la documentación provista en `/data`.
- **Precisión**: El orquestador utiliza un esquema Pydantic estricto para garantizar ruteos correctos.
- **Trazabilidad**: Todas las ejecuciones son monitoreadas en tiempo real mediante Langfuse.
