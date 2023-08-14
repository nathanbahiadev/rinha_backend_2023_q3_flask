# !pip install locust

import random
import string

from locust import HttpUser, task


def gerar_apelido():
    return "".join(random.sample(string.ascii_lowercase, 10))


def gerar_nome():
    return "".join(random.sample(string.ascii_lowercase, 10))


def gerar_stack(minimo: int = 1, maximo: int = 1):
    return random.sample([
            "Python",
            "Go",
            "Javascript",
            "Dart",
            "C#",
            "C",
            "Typescript",
            "Clojure",
            "HTML",
            "CSS",
            "React",
            "JQuery"
        ], random.randint(minimo, maximo))


def gerar_termo():
    funcoes = [
        gerar_nome,
        gerar_apelido,
        lambda: gerar_stack()[0]
    ]
    return random.choices(funcoes)[0]()
    

class RinhaBackendSimulador(HttpUser):
    @task
    def cadastrar_pessoa(self):
        response = self.client.post("/pessoas", json={
            "apelido": gerar_apelido(),
            "nome": gerar_nome(),
            "nascimento": "2000-12-12",
            "stack": gerar_stack(0, 3)
        })

        if location := response.headers.get("Location"):
            self.client.get(location)

    
    # @task
    # def consultar_pessoa(self):
    #     termo = gerar_termo()
    #     self.client.get(f"/pessoas/?t={termo}")
