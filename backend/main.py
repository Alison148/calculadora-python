from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from operations import calcular
from pydantic import BaseModel
from pathlib import Path
import json, time

app = FastAPI(title="Calculadora Científica – Grupo UniAnchieta")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = DATA_DIR / "history.json"

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_history(hist):
    HISTORY_FILE.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")

# estrutura dos itens do histórico
class CalcItem(BaseModel):
    expressao: str
    resultado: float
    modo: str = "DEG"
    ts: float = None

# ====== GET /calcular ======
@app.get("/calcular")
def calcular_expressao(expressao: str, modo: str = "DEG"):
    try:
        resultado = calcular(expressao, modo)
        hist = load_history()
        hist.append(CalcItem(expressao=expressao, resultado=resultado, modo=modo, ts=time.time()).dict())
        save_history(hist)
        return {"expressao": expressao, "resultado": resultado}
    except Exception as e:
        return {"erro": str(e)}

# ====== POST /calcular ======
@app.post("/calcular")
async def calcular_post(request: Request):
    try:
        data = await request.json()
        expressao = data.get("expressao")
        modo = data.get("modo", "DEG")
        resultado = calcular(expressao, modo)
        hist = load_history()
        hist.append(CalcItem(expressao=expressao, resultado=resultado, modo=modo, ts=time.time()).dict())
        save_history(hist)
        return {"expressao": expressao, "resultado": resultado}
    except Exception as e:
        return {"erro": str(e)}

# ====== GET /historico ======
@app.get("/historico")
def obter_historico():
    return {"itens": load_history()}

# ====== DELETE /historico ======
@app.delete("/historico")
def deletar_historico():
    count = len(load_history())
    save_history([])
    return {"mensagem": f"Histórico de {count} cálculos apagado com sucesso."}
