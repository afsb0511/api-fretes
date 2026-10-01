"""
API da 1ª BI - Computação em Nuvem e SOA (Trilha Padrão)
Simulador de fretes + endpoints de carga com complexidades distintas.
"""
import os
import time
import math
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
START = time.time()

# Tabela simples de frete por região (R$/kg) + taxa fixa
TARIFAS = {
    "norte": (4.50, 12.00),
    "nordeste": (5.20, 14.00),
    "centro-oeste": (5.80, 15.00),
    "sudeste": (6.50, 18.00),
    "sul": (7.10, 20.00),
}


@app.get("/")
def index():
    return jsonify(
        servico="API Simulador de Fretes - Computação em Nuvem",
        status="ok",
        uptime_s=round(time.time() - START, 1),
        endpoints=["/health", "/frete", "/o1", "/on", "/on2", "/fib", "/primos"],
    )


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200


@app.get("/frete")
def frete():
    """Ex.: /frete?regiao=norte&peso=10&distancia=500"""
    regiao = request.args.get("regiao", "sudeste").lower()
    try:
        peso = float(request.args.get("peso", 1))
        dist = float(request.args.get("distancia", 100))
    except ValueError:
        return jsonify(erro="peso e distancia devem ser numéricos"), 400
    if regiao not in TARIFAS:
        return jsonify(erro="região inválida", validas=list(TARIFAS)), 400
    por_kg, fixa = TARIFAS[regiao]
    valor = fixa + peso * por_kg + dist * 0.015
    return jsonify(regiao=regiao, peso_kg=peso, distancia_km=dist,
                   valor_total=round(valor, 2))


# ---------- Endpoints de carga: complexidades diferentes (Big-O) ----------
def _n(default, maximo):
    try:
        return max(1, min(int(request.args.get("n", default)), maximo))
    except ValueError:
        return default


@app.get("/o1")
def o1():
    """O(1) - tempo constante."""
    return jsonify(resultado=42)


@app.get("/on")
def on():
    """O(n) - soma linear."""
    n = _n(200_000, 5_000_000)
    return jsonify(n=n, soma=sum(range(n)))


@app.get("/on2")
def on2():
    """O(n^2) - bubble sort (CPU-bound, ótimo para saturar CPU)."""
    n = _n(600, 3000)
    v = [random.random() for _ in range(n)]
    for i in range(n):
        for j in range(n - i - 1):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
    return jsonify(n=n, menor=v[0], maior=v[-1])


@app.get("/fib")
def fib():
    """Fibonacci recursivo - O(2^n) (use n pequeno!)."""
    n = _n(25, 32)

    def f(k):
        return k if k < 2 else f(k - 1) + f(k - 2)

    return jsonify(n=n, fib=f(n))


@app.get("/primos")
def primos():
    """Crivo/contagem de primos por divisão - ~O(n*sqrt(n))."""
    n = _n(20_000, 200_000)
    c = sum(1 for x in range(2, n) if all(x % d for d in range(2, int(math.sqrt(x)) + 1)))
    return jsonify(n=n, total_primos=c)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
