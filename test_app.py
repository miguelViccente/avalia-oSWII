
"""Testes automatizados da API de gerenciamento de tarefas."""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers(client):
    resposta = client.post(
        "/login", json={"usuario": "aluno", "senha": "123456"}
    )
    assert resposta.status_code == 200
    token = resposta.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_consulta_tarefas(client):
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)
    assert resposta.get_json()[0]["titulo"] == "Estudar Flask"


def test_login_correto(client):
    resposta = client.post(
        "/login",
        json={"usuario": "aluno", "senha": "123456"}
    )

    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert isinstance(dados["access_token"], str)
    assert dados["access_token"]


def test_login_senha_incorreta(client):
    resposta = client.post(
        "/login",
        json={"usuario": "aluno", "senha": "errada"}
    )

    assert resposta.status_code == 401
    assert "access_token" not in resposta.get_json()


def test_cadastro_sem_token(client):
    # Consulta a lista antes da tentativa de cadastro
    lista_anterior = client.get("/tarefas").get_json()

    resposta = client.post(
        "/tarefas",
        json={"titulo": "Nova tarefa"}
    )

    assert resposta.status_code == 401

    # Verifica se a lista permaneceu igual
    assert client.get("/tarefas").get_json() == lista_anterior


def test_cadastro_com_token(client, auth_headers):
    lista_anterior = client.get("/tarefas").get_json()

    resposta = client.post(
        "/tarefas",
        json={"titulo": "Nova tarefa"},
        headers=auth_headers
    )

    tarefa = resposta.get_json()

    assert resposta.status_code == 201
    assert tarefa["titulo"] == "Nova tarefa"
    assert tarefa["situacao"] == "pendente"

    # Verifica se o ID é diferente dos anteriores
    ids = [item["id"] for item in lista_anterior]
    assert tarefa["id"] not in ids

    # Confirma que a tarefa foi cadastrada
    lista_atual = client.get("/tarefas").get_json()
    assert tarefa in lista_atual
    assert len(lista_atual) == len(lista_anterior) + 1


@pytest.mark.parametrize("dados", [{}, {"titulo": ""}, {"titulo": "   "}])
def test_cadastro_titulo_vazio(client, auth_headers, dados):
    lista_anterior = client.get("/tarefas").get_json()

    resposta = client.post(
        "/tarefas",
        json=dados,
        headers=auth_headers
    )

    assert resposta.status_code == 400
    assert client.get("/tarefas").get_json() == lista_anterior