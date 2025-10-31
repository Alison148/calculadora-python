import math, re

def calcular(expressao: str, modo: str = "DEG") -> float:
    expressao = expressao.replace("π", "math.pi").replace("pi", "math.pi")
    expressao = expressao.replace("^", "**")
    expressao = expressao.replace(",", ".")
    expressao = expressao.replace("sqrt", "math.sqrt")
    expressao = expressao.replace("%", "/100")

    # Converter trigonometria para graus, se DEG
    if modo.upper() == "DEG":
        expressao = re.sub(r"sin\(([^)]+)\)", r"math.sin(math.radians(\1))", expressao)
        expressao = re.sub(r"cos\(([^)]+)\)", r"math.cos(math.radians(\1))", expressao)
        expressao = re.sub(r"tan\(([^)]+)\)", r"math.tan(math.radians(\1))", expressao)
    else:
        expressao = re.sub(r"sin\(([^)]+)\)", r"math.sin(\1)", expressao)
        expressao = re.sub(r"cos\(([^)]+)\)", r"math.cos(\1)", expressao)
        expressao = re.sub(r"tan\(([^)]+)\)", r"math.tan(\1)", expressao)

    try:
        resultado = eval(expressao, {"__builtins__": None}, {"math": math})
        return round(float(resultado), 10)
    except Exception as e:
        raise ValueError(f"Erro ao calcular: {e}")
