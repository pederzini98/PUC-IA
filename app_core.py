# app_core.py
from __future__ import annotations

ALLOWED_MODELS = {"gemini-1.5-flash", "gemini-1.5-pro"}

def choose_model_name(name: str | None) -> str:
    if not name:
        return "gemini-1.5-flash"
    n = str(name).strip()
    return n if n in ALLOWED_MODELS else "gemini-1.5-flash"

def build_generation_config(temperature: float | int | None) -> dict:
    t = 0.3 if temperature is None else float(temperature)
    if t < 0.0:
        t = 0.0
    if t > 1.0:
        t = 1.0
    return {"temperature": t}

def is_plausible_api_key(value: str | None) -> bool:
    if not value:
        return False
    v = str(value).strip()
    return len(v) >= 10 and " " not in v

def build_diagnose_prompt(lang: str, error_text: str, code_text: str, include_tests: bool) -> str:
    lang = (lang or "python").strip()
    error_text = (error_text or "").strip()
    code_text = (code_text or "").strip()
    include_tests_flag = "Incluir testes: true" if include_tests else "Incluir testes: false"
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

{include_tests_flag}
Linguagem-alvo para exemplos: {lang}.
Erro/stack trace:
{error_text}

Código opcional:
{code_text}
""".strip()
    return prompt
