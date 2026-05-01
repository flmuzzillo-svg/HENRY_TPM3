import os
from .base_agent import SpecializedRAG

class TechAgent(SpecializedRAG):
    """Agente especializado en IT Support."""
    def __init__(self, data_dir: str, vs_dir: str):
        source_file = os.path.join(data_dir, "preguntas_area_tecnica.md")
        persist_dir = os.path.join(vs_dir, "faiss_it")
        super().__init__(name="IT", source_file=source_file, persist_dir=persist_dir)
