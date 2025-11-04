from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
from datetime import datetime

app = FastAPI(title="HelpTech Calculadora Neon API", version="2.0.0")

# Libera acesso do frontend Angular
origins = ["http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# 📜 HISTÓRICO DE CÁLCULOS
# ----------------------------
historico = []

class Operacao(BaseModel):
    operacao: str
    valor1: float
    valor2: float | None = None

# ----------------------------
# 🚀 ROTAS PRINCIPAIS
# ----------------------------
@app.get("/")
def root():
    return {"message": "🚀 API HelpTech Calculadora Neon v2 ativa!"}


@app.post("/calcular")
def calcular_post(dados: Operacao):
    """Recebe via POST um JSON com operacao, valor1 e valor2."""
    return processar_calculo(dados.operacao, dados.valor1, dados.valor2)


@app.get("/calcular")
def calcular_get(
    operacao: str = Query(...),
    valor1: float = Query(...),
    valor2: float | None = None,
):
    """Permite cálculo via GET (ex: /calcular?operacao=+&valor1=5&valor2=3)."""
    return processar_calculo(operacao, valor1, valor2)


# ----------------------------
# ⚙️ FUNÇÃO PRINCIPAL DE CÁLCULO
# ----------------------------
def processar_calculo(operacao: str, valor1: float, valor2: float | None):
    try:
        resultado = None
        op = operacao.lower()

        # Operações básicas
        if op == "+": resultado = valor1 + (valor2 or 0)
        elif op == "-": resultado = valor1 - (valor2 or 0)
        elif op == "*": resultado = valor1 * (valor2 or 0)
        elif op == "/":
            if valor2 == 0:
                return {"erro": "Divisão por zero não é permitida."}
            resultado = valor1 / (valor2 or 1)

        # Trigonometria
        elif op == "sin": resultado = math.sin(math.radians(valor1))
        elif op == "cos": resultado = math.cos(math.radians(valor1))
        elif op == "tan": resultado = math.tan(math.radians(valor1))

        # Avançadas
        elif op == "sqrt": resultado = math.sqrt(valor1)
        elif op == "pow": resultado = math.pow(valor1, valor2 or 2)
        elif op == "log": resultado = math.log(valor1, valor2 or math.e)
        else:
            return {"erro": f"Operação '{operacao}' não suportada."}

        registro = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "operacao": operacao,
            "valor1": valor1,
            "valor2": valor2,
            "resultado": resultado,
        }
        historico.append(registro)
        return registro

    except Exception as e:
        return {"erro": str(e)}


# ----------------------------
# 📘 HISTÓRICO: GET / POST / DELETE
# ----------------------------
@app.get("/historico")
def listar_historico():
    """Retorna todo o histórico de cálculos."""
    return {"quantidade": len(historico), "dados": historico}


@app.post("/historico/limpar")
@app.delete("/historico")
def limpar_historico():
    """Limpa o histórico."""
    historico.clear()
    return {"mensagem": "🧹 Histórico limpo com sucesso!", "quantidade": 0}
