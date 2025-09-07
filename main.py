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

st.set_page_config(page_title="Projeto Final - Agente IA p/ Engenharia de Software", page_icon="🤖", layout="wide")

st.title("🤖 Agente IA — Diagnóstico e Automação para Engenharia de Software")
st.caption("MVP: Diagnóstico de erros + sugestões de correção • Powered by Google Gemini")

with st.sidebar:
    st.header("⚙️ Configurações")
    if not API_KEY:
        st.error("Variável de ambiente GOOGLE_API_KEY não encontrada. Crie um arquivo `.env` com a chave.")
    model_name = st.selectbox("Modelo Gemini", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.3, 0.1)
    st.markdown("---")
    st.subheader("📋 Briefing (resumo)")
    st.markdown("""
**Nome dos Alunos:** _preencha aqui no README e/ou apresentação_  
**Nome do Projeto:** **BugSage** – Agente de Diagnóstico e Refatoração para Devs  
**Problema:** diagnóstico de erros comuns (stack traces, exceptions) e apoio à correção/refatoração, geração de testes e documentação.  
**Usuário-alvo:** desenvolvedores (júnior a sênior), QAs e tech leads.  
**MVP:** usuário cola erro e/ou código → IA explica a causa, propõe correção (patch) e testes.  
    """)

# Configure Gemini com tratamento de erro simples
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
            generation_config={"temperature": temperature}
        )
        return resp.text
    except Exception as e:
        return f"⚠️ Erro ao chamar o modelo: {e}"

# ---------------------------
# UI
# ---------------------------
tab_mvp, tab_refac, tab_tests, tab_docs, tab_chat = st.tabs([
    "MVP — Diagnóstico de Erros",
    "Refatoração de Código",
    "Geração de Testes",
    "Documentação Automática",
    "Chat Livre"
])

with tab_mvp:
    st.subheader("🚨 Cole um stack trace, mensagem de erro e/ou trecho de código")
    lang = st.selectbox("Linguagem (para formatação do patch/código)", ["python", "go", "csharp", "java", "javascript", "sql", "bash"], index=0)
    error_text = st.text_area("Erro / Stack trace", height=180, placeholder="Ex.: Traceback (most recent call last): ...")
    code_text = st.text_area("Código relacionado (opcional)", height=220, placeholder=f"```{lang}\n# cole aqui\n```")
    uploaded = st.file_uploader("Ou envie um arquivo de log/código (txt, log, py, go, cs, js, java)", type=["txt","log","py","go","cs","js","java"])
    if uploaded is not None and not code_text and not error_text:
        try:
            code_text = uploaded.read().decode("utf-8", errors="ignore")
            st.info("Arquivo carregado. Conteúdo adicionado ao campo de código/erro.")
        except Exception:
            st.warning("Não foi possível ler o arquivo enviado.")

    col1, col2 = st.columns([1,1])
    with col1:
        diagnose = st.button("🔍 Diagnosticar & Sugerir Correção", type="primary")
    with col2:
        add_tests = st.checkbox("Incluir sugestões de testes automáticos", value=True)

    if diagnose:
        prompt = f"""
Usuário forneceu um erro/stack trace e opcionalmente um trecho de código.

Tarefa:
1) Explicar a causa provável do erro (top 1-3 hipóteses);
2) Passos de diagnóstico para confirmar;
3) Propor correção com **patch** (unified diff) e também mostrando o código final;
4) Se `Incluir testes` estiver marcado, gerar testes mínimos executáveis para o cenário;
5) Alertar sobre impactos/edge cases.

Formato de saída:
- **Análise** (bullets curtas)
- **Passos de diagnóstico**
- **Correção (patch)**
- **Código final**
- **Testes sugeridos** (se aplicável)

Linguagem-alvo para exemplos: {lang}.
Erro/stack trace:
{error_text}

Código opcional:
{code_text}
"""
        extras = {"language": lang, "include_tests": add_tests}
        with st.spinner("Analisando com Gemini..."):
            output = call_gemini(prompt, extras)
        st.markdown(output)

with tab_refac:
    st.subheader("🛠️ Refatorar código")
    lang2 = st.selectbox("Linguagem do código", ["python", "go", "csharp", "java", "javascript"], index=0, key="ref_lang")
    goals = st.multiselect("Objetivos da refatoração", ["Legibilidade", "Performance", "Segurança", "Testabilidade", "Padronização (lint/estilo)"], default=["Legibilidade","Testabilidade"])
    code_in = st.text_area("Cole o código", height=260, placeholder=f"```{lang2}\n# seu código aqui\n```")
    if st.button("Refatorar", type="primary"):
        prompt = f"""
Refatore o código abaixo com foco em {', '.join(goals)}.
- Explique rapidamente as mudanças mais importantes.
- Mostre o **diff** (unified) e o código final.
- Evite mudanças desnecessárias.

Linguagem: {lang2}
Código:
{code_in}
"""
        with st.spinner("Refatorando com Gemini..."):
            st.markdown(call_gemini(prompt))

with tab_tests:
    st.subheader("🧪 Gerar testes unitários")
    lang3 = st.selectbox("Linguagem/Framework alvo", ["python/pytest", "go/testing", "csharp/xUnit", "java/junit5", "javascript/jest"], index=0)
    code_for_test = st.text_area("Código-fonte alvo", height=260)
    if st.button("Gerar testes"):
        prompt = f"""
Gere testes unitários para o seguinte código.
- Crie casos positivos e negativos.
- Dê instruções de execução (ex.: pytest -q, go test, dotnet test, mvn test, npm test).
- Informe mocks/stubs necessários.
Alvo: {lang3}

Código:
{code_for_test}
"""
        with st.spinner("Gerando testes com Gemini..."):
            st.markdown(call_gemini(prompt))

with tab_docs:
    st.subheader("📚 Documentação automática")
    lang4 = st.selectbox("Linguagem principal", ["python", "go", "csharp", "java", "javascript"], index=0, key="doc_lang")
    doc_style = st.selectbox("Estilo de docstring", ["Google", "NumPy", "reST", "JSDoc", "XML (C#)"], index=0)
    code_doc = st.text_area("Cole o código para documentar", height=260)
    if st.button("Gerar documentação"):
        prompt = f"""
Gere documentação para o código a seguir:
- Adicione docstrings no estilo {doc_style}.
- Gere um README curto explicando objetivo, uso e requisitos.
- Liste limitações conhecidas e TODOs.

Linguagem: {lang4}
Código:
{code_doc}
"""
        with st.spinner("Gerando documentação com Gemini..."):
            st.markdown(call_gemini(prompt))

with tab_chat:
    st.subheader("💬 Chat livre")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_msg = st.chat_input("Pergunte algo sobre engenharia de software, logs, testes, etc.")
    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        prompt = f"Converse tecnicamente e de forma didática. Pergunta do usuário: {user_msg}"
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                answer = call_gemini(prompt)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
