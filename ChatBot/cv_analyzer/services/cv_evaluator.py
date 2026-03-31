from langchain_openai import ChatOpenAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts


def crear_evaluador_cv():
    base_model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    structure_model = base_model.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    evaluation_chain = chat_prompt | structure_model

    return evaluation_chain

def candidate_evaluation(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        evaluation_chain = crear_evaluador_cv()

        resultado = evaluation_chain.invoke({

            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        return resultado
    
    except Exception as e:
        return AnalisisCV(
            candidate_name=f"Error: {str(e)}"

        )

