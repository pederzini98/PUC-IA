# Projeto Final — BugSage (Agente IA para Engenharia de Software)

## Como rodar
```bash
pip install -U -r requirements.txt
streamlit run main.py
```

Defina `GOOGLE_API_KEY` no `.env`.

---

## 🚢 Deploy & Dev/CI

### Docker
```bash
docker build -t bugsage:local .
docker run -it --rm -p 8501:8501 -e GOOGLE_API_KEY=SUACHAVEAQUI bugsage:local
```

### GitHub Actions (CI)
- Workflow em `.github/workflows/ci.yml` roda `pytest` e um **smoke test** com `streamlit run` headless.

### GitHub Codespaces
- Config em `.devcontainer/devcontainer.json`.
- Rodar: `streamlit run main.py`

### Terraform (demo EC2 + S3)
- Infra de exemplo em `terraform/`.
