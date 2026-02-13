# 🔍 Incident Analysis with Python & SQL

Projeto prático de **análise de incidentes de segurança**, simulando a rotina de um analista SOC.  
Desenvolvido com Python + Pandas + SQLite, o pipeline lê, processa e gera relatórios automáticos a partir de dados simulados de incidentes.

---

## 🚀 Resultado da Execução

Ao rodar o projeto, você obtém:

🚀 Starting Incident Analysis with Python & SQL
✅ Done!
📦 Database: data/incidents.db
📄 Report: reports/report.txt

Quick summary:
Total incidents: 120
Top severities: High:47, Medium:28, Low:26, Critical:19


> ✅ Projeto funcional e testado no macOS e Linux.

---

## 🎯 Objetivo

Entregar uma ferramenta simples e funcional que:
- Organiza dados brutos de incidentes
- Identifica eventos críticos por severidade
- Agrupa e conta ocorrências
- Gera relatório resumido para tomada de decisão

---

## 🛠️ Tecnologias

- Python 3.11+
- Pandas (análise de dados)
- SQLite (banco local)
- Git / GitHub

---

## 📂 Estrutura

📁 data/ → Base de dados SQLite
📁 reports/ → Relatórios gerados (.txt)
📁 src/ → Código fonte
└── main.py → Pipeline principal


---

## ▶️ Como executar

```bash
git clone https://github.com/sejosegomesneto-creator/incident-analysis-python-sql
cd incident-analysis-python-sql
python3 -m venv venv
source venv/bin/activate
pip3 install pandas
python3 src/main.py
