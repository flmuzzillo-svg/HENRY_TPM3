import os
from .base_agent import SpecializedRAG

class FinanceAgent(SpecializedRAG):
    """Agente especializado en Finanzas."""
    def __init__(self, data_dir: str, vs_dir: str):
        source_file = os.path.join(data_dir, "preguntas_finanzas.md")
        persist_dir = os.path.join(vs_dir, "faiss_finance")
        super().__init__(name="FINANCE", source_file=source_file, persist_dir=persist_dir)
