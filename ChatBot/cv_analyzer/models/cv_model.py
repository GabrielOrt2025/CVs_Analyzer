
from pydantic import BaseModel, Field


"""Este es un docstring"""
class AnalisisCV(BaseModel):
    """Este es un docstring"""
    candidate_name: str = Field(description = "Nombre completo del candidatos extraido del CV.")
    experience: int = Field(description = "anios toyales de experiencia laboral relevante")
    key_habilities: list[str] = Field(description = "Lista de las 5-7 habilidades del candidato mas relevantes para el puesto.")
    education: str = Field(description = "Nivel educativo mas alto y especializazcion principal")
    relevant_experience: str = Field(description = "Experiencia mas relevante para el puesto en especifico")
    strengths: list[str] = Field(description = "3-5 principales fortalezas del candidato basadas en su perfil")
    improvemnts: list[str] = Field(description = "2-4 areas donde el candidato podria mejorar" )
    porcentaje: int = Field(description = "Porcentaje de ajuste al puesto (0-100) basado en la experiencia, habilidades y formacion.", ge=0, le=100)