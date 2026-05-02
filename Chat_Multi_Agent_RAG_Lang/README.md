# Sistema Multi-Agente RAG (Version OpenAI)

## Descripcion del Proyecto

Este proyecto implementa un sistema RAG avanzado que utiliza agentes especializados para responder consultas sobre Recursos Humanos, Finanzas y Tecnología. Utiliza el stack nativo de OpenAI para garantizar la máxima coherencia y facilidad de integración. El flujo se basa en un orquestador que clasifica la intención y activa la cadena RAG del agente correspondiente.

## Arquitectura

```
Usuario -> Orquestador (GPT-4o) -> Agente Experto (RAG) -> Respuesta
                                        |
                            [FAISS Store + Contexto MD]
```

## Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| API Provider | OpenAI |
| Embeddings | OpenAI `text-embedding-3-small` |
| Generacion | `gpt-4o` |
| Vector Store | FAISS |
| Framework | LangChain (LCEL) |
| Observabilidad | Langfuse |

## Configuracion e Instalacion

### Paso 1: Dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Variables de Entorno
Configura tu archivo `.env`:
```env
OPENAI_API_KEY=tu_clave_aqui
LANGFUSE_PUBLIC_KEY=tu_clave
LANGFUSE_SECRET_KEY=tu_clave
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Ejecucion

Para ejecutar las pruebas automáticas del sistema:
```bash
python src/multi_agent_system.py
```

## Justificacion de Herramientas

- **FAISS**: Elegido por su velocidad extrema en búsquedas de similitud vectorial de forma local, ideal para conjuntos de datos corporativos de tamaño medio.
- **LCEL (LangChain Expression Language)**: Permite una composición de cadenas más clara, manejo de streaming nativo y trazabilidad automática.
- **Langfuse**: Proporciona un dashboard detallado para auditar los costos de tokens y la latencia de cada agente.

## Metricas de Calidad
- **Indexacion**: Se procesan múltiples archivos Markdown (`preguntas_*.md`).
- **Evaluacion**: Incluye un script de evaluación que registra scores automáticos en Langfuse basados en la relevancia de la respuesta.
