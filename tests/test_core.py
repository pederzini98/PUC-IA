# tests/test_core.py
from app_core import choose_model_name, build_generation_config, is_plausible_api_key, build_diagnose_prompt

def test_choose_model_name_defaults():
    assert choose_model_name(None) == "gemini-1.5-flash"
    assert choose_model_name("invalid-model") == "gemini-1.5-flash"
    assert choose_model_name("gemini-1.5-pro") == "gemini-1.5-pro"

def test_build_generation_config_bounds():
    assert build_generation_config(-1.0)["temperature"] == 0.0
    assert build_generation_config(2.0)["temperature"] == 1.0
    assert 0.0 <= build_generation_config(0.42)["temperature"] <= 1.0

def test_is_plausible_api_key():
    assert not is_plausible_api_key(None)
    assert not is_plausible_api_key("")
    assert not is_plausible_api_key("short")
    assert not is_plausible_api_key("with space key 12345")
    assert is_plausible_api_key("A1B2C3D4E5F6G7H8I9J0")

def test_build_diagnose_prompt_structure():
    p = build_diagnose_prompt("python", "Traceback: boom", "print('x')", True)
    assert "Análise" in p
    assert "Passos de diagnóstico" in p
    assert "Correção (patch)" in p
    assert "Código final" in p
    assert "Testes sugeridos" in p
    assert "Linguagem-alvo para exemplos: python" in p
    assert "Traceback: boom" in p
    assert "print('x')" in p
