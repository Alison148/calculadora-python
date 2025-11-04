# ⚡ HelpTech Calculadora Neon

Uma calculadora científica moderna desenvolvida com **Angular 17 + FastAPI (Python)**.  
Tema escuro com **azul neon (#00d9ff)**, design responsivo e efeito glow.

---

## 🚀 Rodar o Backend (FastAPI)
```bash
cd backend
Windows
venv\Scripts\activate

Instalar dependências pip install -r requirements.txt

Rodar servidor (modo dev) uvicorn main:app --reload --host 0.0.0.0 --port 8000

Acessar no navegador

Swagger: http://127.0.0.1:8000/docs

💻 Rodar o Frontend (Angular)
bash
Copiar código
cd frontend
npm install
ng serve
Acesse: http://localhost:4200

🧮 Operações Suportadas
Categoria	Operações
Básicas	+, -, *, /
Trigonométricas	sin, cos, tan
Avançadas	sqrt, pow, log

🧩 Estrutura do Projeto
css
Copiar código
helptech_calculadora_neon/
├── backend/             → FastAPI API
├── frontend/            → Angular App
├── start_calculadora.bat → Inicia backend + frontend
├── gerar_zip.bat         → Compacta o projeto
└── extrair_zip.bat       → Extrai o projeto e abre no VS Code
Desenvolvido por HelpTech Antunes © 2025 💙

yaml
Copiar código

---

## ⚙️ **gerar_zip.bat**
```bat
@echo off
title Compactar Projeto HelpTech Calculadora Neon
echo ==============================================
echo   Criando helptech_calculadora_neon.zip...
echo ==============================================

if exist helptech_calculadora_neon.zip del helptech_calculadora_neon.zip
powershell Compress-Archive -Path "helptech_calculadora_neon" -DestinationPath "helptech_calculadora_neon.zip"

echo ✅ Arquivo ZIP criado com sucesso!
pause
⚙️ extrair_zip.bat
bat
Copiar código
@echo off
title Extrair HelpTech Calculadora Neon
echo ==============================================
echo   Extraindo helptech_calculadora_neon.zip...
echo ==============================================

if not exist helptech_calculadora_neon.zip (
    echo ❌ O arquivo ZIP nao foi encontrado!
    pause
    exit /b
)

if exist helptech_calculadora_neon (
    echo ⚠️ Removendo pasta antiga...
    rmdir /s /q helptech_calculadora_neon
)

powershell Expand-Archive -Path "helptech_calculadora_neon.zip" -DestinationPath "helptech_calculadora_neon"

where code >nul 2>nul
if %errorlevel%==0 (
    echo 🧠 Abrindo o projeto no Visual Studio Code...
    start code helptech_calculadora_neon
)
echo ✅ Projeto extraido com sucesso!
pause
