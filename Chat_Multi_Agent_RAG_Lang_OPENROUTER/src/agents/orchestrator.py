import os
from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class RouteClassification(BaseModel):
    intent: Literal["HR", "IT", "FINANCE", "UNKNOWN"] = Field(
        description="El departamento destino al que se debe enrutar la pregunta del usuario. Debe ser HR, IT, FINANCE o UNKNOWN."
    )

class RouterAgent:
    """Orquestador para enrutar consultas al agente especialista adecuado."""
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-oss-120b",
            temperature=0,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.parser = PydanticOutputParser(pydantic_object=RouteClassification)
        
        system_prompt = (
            "Eres un clasificador de intenciones experto. Dada una pregunta del usuario, tu tarea es enrutarla "
            "al departamento especializado correcto: HR (Recursos Humanos), IT (Tecnología) o FINANCE (Finanzas). "
            "Si la pregunta no corresponde a ninguno de estos departamentos, enrútala a UNKNOWN.\n"
            "CRÍTICO: Devuelve ÚNICAMENTE JSON sin formato. Sin bloques de código, sin comillas adicionales, sin texto extra.\n"
            "{format_instructions}"
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])
        
        self.chain = self.prompt | self.llm | self.parser

    async def aroute(self, question: str, callbacks: list) -> str:
        try:
            response = await self.chain.ainvoke(
                {
                    "question": question, 
                    "format_instructions": self.parser.get_format_instructions()
                },
                config={"callbacks": callbacks}
            )
            return response.intent
        except Exception as e:
            print(f"[Router Fallback] Falló el parseo JSON estricto, intentando extracción básica...")
            res = await self.llm.ainvoke(
                f"Classify the following question into exactly one of these categories: HR, IT, FINANCE, UNKNOWN.\n"
                f"Question: {question}\n"
                f"Return ONLY the category name, nothing else."
            )
            text = res.content.upper()
            for intent in ["HR", "IT", "FINANCE"]:
                if intent in text:
                    return intent
            return "UNKNOWN"
