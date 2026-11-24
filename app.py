
"""API de gerenciamento de tarefas - Avaliação de SW II."""
import os
from datetime import timedelta

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        JWT_SECRET_KEY=os.environ.get(
            "JWT_SECRET_KEY", "chave-didatica-local-sw-ii-nao-usar-em-producao"
        ),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
    )

    if test_config:
        app.config.update(test_config)

    jwt = JWTManager(app)

    tarefas = [{"id": 1, "titulo": "Estudar Flask", "situacao": "pendente"}]

    usuarios = {
        "aluno": generate_password_hash("123456")
    }

    @jwt.unauthorized_loader
    def token_ausente(motivo):
        return jsonify({"erro": "Token de acesso ausente."}), 401

    @jwt.invalid_token_loader
    def token_invalido(motivo):
        return jsonify({"erro": "Token de acesso inválido."}), 401

    @jwt.expired_token_loader
    def token_expirado(header, payload):
        return jsonify({"erro": "Token de acesso expirado."}), 401

    @app.post("/login")
    def login():
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON."}), 400

        usuario = dados.get("usuario")
        senha = dados.get("senha")

        if not isinstance(usuario, str) or not isinstance(senha, str):
            return jsonify({"erro": "Informe usuário e senha como texto."}), 400

        # Busca a senha armazenada como hash
        senha_hash = usuarios.get(usuario)

        # Verifica as credenciais
        if senha_hash is None or not check_password_hash(senha_hash, senha):
            return jsonify({"erro": "Usuário ou senha incorretos."}), 401

        # Gera o token de acesso
        token = create_access_token(identity=usuario)

        return jsonify({"access_token": token}), 200

    @app.get("/tarefas")
    def listar_tarefas():
        return jsonify(tarefas), 200

    @app.post("/tarefas")
    @jwt_required()
    def cadastrar_tarefa():
        dados = request.get_json(silent=True)

        if not isinstance(dados, dict):
            return jsonify({"erro": "Envie um objeto JSON."}), 400

        # Obtém e valida o título
        titulo = dados.get("titulo")

        if not isinstance(titulo, str) or not titulo.strip():
            return jsonify({"erro": "O título é obrigatório."}), 400

        titulo = titulo.strip()

        # Gera um identificador único
        novo_id = max((tarefa["id"] for tarefa in tarefas), default=0) + 1

        # Cria a nova tarefa
        nova_tarefa = {
            "id": novo_id,
            "titulo": titulo,
            "situacao": "pendente"
        }

        tarefas.append(nova_tarefa)

        return jsonify(nova_tarefa), 201

    return app


if __name__ == "__main__":
    create_app().run(debug=True)