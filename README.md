# Projeto 1ª BI - Computação em Nuvem e SOA

Estrutura:
```
app.py  requirements.txt  Dockerfile  .dockerignore  locust/locustfile.py
```

## 1) Rodar local sem Docker (opcional)
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                    # http://localhost:8000
```

## 2) Rodar com Docker (Prática 1 - print do container local)
```bash
docker build -t api-fretes .
docker run -d --name api-fretes -p 8000:8000 api-fretes
curl http://localhost:8000/health
curl "http://localhost:8000/frete?regiao=norte&peso=10&distancia=500"
docker ps          # print para o relatório
docker logs api-fretes
docker stats       # acompanhe CPU/RAM durante o Locust
```

## 3) GitHub
```bash
git init && git add . && git commit -m "API fretes 1a BI"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/api-fretes.git
git push -u origin main      # repositório PÚBLICO
```

## 4) Deploy no Render (PaaS, HTTPS automático)
1. Acesse render.com -> New -> Web Service -> conecte o repositório.
2. Runtime: **Docker** (ele detecta o Dockerfile). Plano: Free.
3. Deploy. A URL será https://NOME.onrender.com
4. Teste: `curl -i https://NOME.onrender.com/health` (deve retornar HTTP 200 OK - print!)
Obs.: no plano free o serviço "dorme" após inatividade; abra a URL 1-2 min antes do pitch.

Alternativas: Railway (New Project -> Deploy from GitHub) ou AWS App Runner.

## 5) Testes de carga com Locust (Prática 2)
```bash
pip install locust
# Linha de base LOCAL: 50 usuários
locust -f locust/locustfile.py --host http://localhost:8000
# abra http://localhost:8089 -> Users: 50, Spawn rate: 5 -> Start
```
Estresse em NUVEM: mesmo comando com `--host https://NOME.onrender.com`,
Users: **200**, Spawn rate: 10. Rode ~3 min e tire print das abas
Statistics, Charts (RPS, tempos de resposta, usuários) e Failures.

Modo headless + CSV (para gerar gráficos depois):
```bash
locust -f locust/locustfile.py --host https://NOME.onrender.com \
  --headless -u 200 -r 10 -t 3m --csv resultados_nuvem
```
Os valores p95/p99 aparecem em Statistics e no CSV.

## 6) Roteiro do Pitch (10 min)
1. (2 min) Arquitetura: Cliente -> HTTPS PaaS -> container (gunicorn 2 workers x 4 threads) -> Flask. Mostre a URL.
2. (3 min) Dispare o Locust ao vivo contra a URL pública (200 usuários).
3. (2 min) Explique RPS, p95/p99, taxa de erro e o limite de CPU/RAM do plano free.
4. (3 min) Arguição - veja abaixo.

## 7) Ideias para a análise e arguição
- **Big-O**: /o1 (constante), /on (linear), /on2 (quadrático, satura a CPU), /fib (exponencial). Compare latências no Locust.
- **Amdahl**: Speedup = 1 / ((1-P) + P/N). Com 2 workers e plano de ~0,1-0,5 vCPU, o ganho é limitado pela parte serial e pelo limite físico de CPU.
- **Gargalo**: /on2 é CPU-bound; sob 200 usuários o p99 dispara e aparecem timeouts/5xx.
- **Elasticidade**: no plano free do Render não há autoscaling (instância única). Em planos pagos, ou App Runner, há escalonamento horizontal por concorrência/CPU. Diga isso com honestidade no relatório.
- **Por que gunicorn e não `flask run`?** Servidor WSGI de produção, múltiplos workers/threads.
- **Por que Alpine?** Imagem menor (~50 MB), menor superfície de ataque.
