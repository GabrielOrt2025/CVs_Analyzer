import streamlit as st
from services.cv_evaluator import candidate_evaluation
from models.cv_model import AnalisisCV
from services.pdf_processor import extract_text_pdf

def main():
    """Función principal que define la interfaz de usuario de Streamlit"""

    st.set_page_config(
        page_title="Sistema de Evaluación de CVs",
        layout="wide"
    )

    st.title("Sistema de Evaluación de Candidatos")
    st.caption("Análisis automatizado de currículums utilizando inteligencia artificial")

    st.markdown("""
    Esta herramienta permite analizar currículums en formato PDF y evaluar el nivel de ajuste
    de un candidato respecto a un puesto específico, considerando experiencia, habilidades
    y formación académica.
    """)

    st.divider()

    col_entrada, col_resultado = st.columns([1, 1], gap="large")

    with col_entrada:
        procesar_entrada()

    with col_resultado:
        mostrar_area_resultados()


def procesar_entrada():
    """Maneja la entrada de datos del usuario"""

    st.subheader("Datos de entrada")

    archivo_cv = st.file_uploader(
        "Currículum del candidato (PDF)",
        type=['pdf']
    )

    if archivo_cv is not None:
        st.success(f"Archivo cargado correctamente: {archivo_cv.name}")
        st.caption(f"Tamaño: {archivo_cv.size:,} bytes")

    st.markdown("---")

    descripcion_puesto = st.text_area(
        "Descripción del puesto",
        height=250,
        placeholder="Describe los requisitos, responsabilidades y habilidades necesarias..."
    )

    st.markdown("---")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        analizar = st.button(
            "Analizar candidato",
            type="primary",
            use_container_width=True
        )

    with col_btn2:
        if st.button("Limpiar", use_container_width=True):
            st.rerun()

    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['descripcion_puesto'] = descripcion_puesto
    st.session_state['analizar'] = analizar


def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""

    st.subheader("Resultados del análisis")

    if st.session_state.get('analizar', False):
        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()

        if archivo_cv is None:
            st.error("Debe cargar un archivo PDF del currículum")
            return

        if not descripcion_puesto:
            st.error("Debe proporcionar una descripción del puesto")
            return

        procesar_analisis(archivo_cv, descripcion_puesto)
    else:
        st.info("""
        Para iniciar el análisis:

        1. Cargue un currículum en formato PDF  
        2. Ingrese la descripción del puesto  
        3. Presione el botón "Analizar candidato"
        """)


def procesar_analisis(archivo_cv, descripcion_puesto):
    """Procesa el análisis completo del CV"""

    with st.spinner("Procesando información..."):

        texto_cv = extract_text_pdf(archivo_cv)

        if texto_cv.startswith("Error"):
            st.error(texto_cv)
            return

        resultado = candidate_evaluation(texto_cv, descripcion_puesto)

        mostrar_resultados(resultado)


def mostrar_resultados(resultado: AnalisisCV):
    """Muestra los resultados del análisis de manera estructurada"""

    st.subheader("Evaluación general")

    st.metric(
        label="Nivel de ajuste",
        value=f"{resultado.porcentaje}%"
    )

    if resultado.porcentaje >= 70:
        st.success("El candidato presenta un alto nivel de compatibilidad con el puesto.")
    elif resultado.porcentaje >= 50:
        st.warning("El candidato presenta compatibilidad parcial con el puesto.")
    else:
        st.error("El candidato no cumple con los requisitos principales del puesto.")

    st.divider()

    st.subheader("Información del candidato")

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Nombre:** {resultado.candidate_name}")
        st.write(f"**Experiencia:** {resultado.experience} años")

    with col2:
        st.write(f"**Formación académica:** {resultado.education}")

    st.subheader("Experiencia relevante")
    st.write(resultado.relevant_experience)

    st.divider()

    st.subheader("Habilidades técnicas")
    if resultado.key_habilities:
        for habilidad in resultado.key_habilities:
            st.write(f"- {habilidad}")
    else:
        st.write("No se identificaron habilidades relevantes.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Fortalezas")
        if resultado.strengths:
            for f in resultado.strengths:
                st.write(f"- {f}")
        else:
            st.write("No se identificaron fortalezas.")

    with col2:
        st.subheader("Áreas de mejora")
        if resultado.improvemnts:
            for m in resultado.improvemnts:
                st.write(f"- {m}")
        else:
            st.write("No se identificaron áreas de mejora.")

    st.divider()

    if st.button("Guardar análisis"):
        st.info("Funcionalidad en desarrollo")