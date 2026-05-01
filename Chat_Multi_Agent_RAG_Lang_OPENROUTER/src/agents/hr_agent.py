import os
from .base_agent import SpecializedRAG

class HRAgent(SpecializedRAG):
    """Agente especializado en Recursos Humanos."""
    def __init__(self, data_dir: str, vs_dir: str):
        source_file = os.path.join(data_dir, "preguntas_rrhh.md")
        persist_dir = os.path.join(vs_dir, "faiss_hr")
        super().__init__(name="HR", source_file=source_file, persist_dir=persist_dir)
