import os
import sys
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class SpecializedRAG:
    """Base class for specialized RAG agents."""
    
    def __init__(self, name: str, source_file: str, persist_dir: str):
        self.name = name
        self.source_file = source_file
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatOpenAI(
            model="gpt-oss-120b",
            temperature=0,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        
        self.vector_store = self._load_or_create_index()
        self.retriever = self.vector_store.as_retriever()
        
        # Crear cadena RAG
        system_prompt = (
            "You are an assistant for question-answering tasks for the {name} department. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt.format(name=self.name, context="{context}")),
            ("human", "{input}"),
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
            
        self.rag_chain = (
            {"context": self.retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def _load_or_create_index(self):
        if os.path.exists(self.persist_dir):
            print(f"[{self.name}] Cargando índice FAISS desde disco ({self.persist_dir})...")
            return FAISS.load_local(self.persist_dir, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print(f"[{self.name}] Creando nuevo índice FAISS desde {self.source_file}...")
            loader = UnstructuredMarkdownLoader(self.source_file)
            docs = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            splits = text_splitter.split_documents(docs)
            
            total_splits = len(splits)
            print(f"[{self.name}] Carga de Embeddings iniciada para {total_splits} fragmentos...")
            vector_store = None
            batch_size = max(1, total_splits // 10)
            
            for i in range(0, total_splits, batch_size):
                batch = splits[i:i+batch_size]
                if vector_store is None:
                    vector_store = FAISS.from_documents(batch, self.embeddings)
                else:
                    vector_store.add_documents(batch)
                
                progress = min(100, int((i + len(batch)) / total_splits * 100))
                sys.stdout.write(f"\r[{self.name}] Progreso de embeddings: {progress}% completado")
                sys.stdout.flush()
            print()
            vector_store.save_local(self.persist_dir)
            return vector_store

    async def aquery(self, question: str, callbacks: list) -> str:
        print(f"[{self.name}] Procesando consulta...")
        response = await self.rag_chain.ainvoke(
            question,
            config={"callbacks": callbacks}
        )
        return response
