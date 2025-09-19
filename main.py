# main.py
import os
import json
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Gemini SDK
import google.generativeai as genai

# ---------------------------
# Setup
# ---------------------------
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

st.set_page_config(
    page_title="Projeto Final - Agente IA p/ Engenharia de Software",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 BugSage")

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.header("⚙️ Configurações")
    if not API_KEY:
        st.error("Variável de ambiente GOOGLE_API_KEY não encontrada. Crie um arquivo `.env` com a chave.")

    model_name = st.selectbox("Modelo Gemini", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.3, 0.1)



    st.markdown("---")
    # Menu sem tabs
    view = st.radio(
        "Navegação",
        ["🧪 Gerar testes unitários"],  # adicione outras telas aqui depois, se quiser
        index=0,
    )

# ---------------------------
# Gemini helpers
# ---------------------------
def _configure_model():
    if not API_KEY:
        return None
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel(model_name)
    except Exception:
        return None

SYSTEM_INSTRUCTIONS = """Você é um assistente técnico para engenharia de software.
- Seja direto, estruturado e didático.
- Quando gerar código, use blocos com a linguagem correta (```python, ```go, ```csharp, ```java, ```js).
- Quando propor correções, sempre inclua um *patch* em formato unified diff quando fizer sentido.
- Para testes, proponha skeletons mínimos executáveis.
- Se o usuário subir logs/stack traces, identifique causa raiz provável e passos de diagnóstico.
- Nunca invente APIs que não existem; se houver incerteza, declare explicitamente.
"""

def call_gemini(prompt: str, extras: dict | None = None):
    if not API_KEY:
        return "❌ GOOGLE_API_KEY ausente. Edite `.env` e recarregue."
    try:
        model = _configure_model()
        if not model:
            return "❌ Não foi possível inicializar o modelo. Verifique a chave e a versão do SDK."
        content_parts = [SYSTEM_INSTRUCTIONS, "\n\n---\n", prompt]
        if extras:
            content_parts.append("\n\nContexto extra:\n")
            content_parts.append(json.dumps(extras, ensure_ascii=False, indent=2))
        resp = model.generate_content(
            content_parts,
            generation_config={"temperature": float(temperature)},
        )
        return getattr(resp, "text", "⚠️ Resposta vazia do modelo.")
    except Exception as e:
        return f"⚠️ Erro ao chamar o modelo: {e}"

    
# ---------------------------
# Views (sem tabs)
# ---------------------------
def render_tests_view():
    st.subheader("Seu gerador de testes unitários com Gemini!")
    st.markdown("""
                Cole um código que eu vou te poupar o trabalho dos testes hehe.
                """)
    lang = st.selectbox(
        "Linguagem/Framework alvo",
        ["python/pytest", "go/testing", "csharp/xUnit", "java/junit5", "javascript/jest"],
        index=0,
    )
    code_for_test = st.text_area("Código-fonte alvo", height=260, placeholder="Cole aqui o código...")
    generate = st.button("Gerar testes")
    if generate:
        prompt = f"""
Gere testes unitários para o seguinte código.
- Crie casos positivos e negativos.
- Dê instruções de execução (ex.: pytest -q, go test, dotnet test, mvn test, npm test).
- Informe mocks/stubs necessários.
Alvo: {lang}

Código:
{code_for_test}
"""
        with st.spinner("Gerando testes com Gemini..."):
            st.markdown(call_gemini(prompt))

# Router simples
if view == "🧪 Gerar testes unitários":
    render_tests_view()
