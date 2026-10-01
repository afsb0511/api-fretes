"""
Uso:
  locust -f locust/locustfile.py --host http://localhost:8000
  locust -f locust/locustfile.py --host https://SEU-APP.onrender.com
"""
import random
from locust import HttpUser, task, between


class UsuarioAPI(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def frete(self):
        regiao = random.choice(["norte", "nordeste", "sudeste", "sul", "centro-oeste"])
        self.client.get(f"/frete?regiao={regiao}&peso={random.randint(1,50)}&distancia={random.randint(50,3000)}",
                        name="/frete")

    @task(3)
    def o1(self):
        self.client.get("/o1")

    @task(2)
    def on(self):
        self.client.get("/on?n=200000", name="/on")

    @task(1)
    def on2(self):
        # endpoint pesado: gera gargalo de CPU
        self.client.get("/on2?n=400", name="/on2")
