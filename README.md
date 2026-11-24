# Avaliação prática — SW II

## Desafio
Complete a API de tarefas e os testes em quatro aulas de 50 minutos, em dupla.
O projeto é uma base intencionalmente incompleta: os TODOs são parte da avaliação.

## Preparação (Windows / PowerShell)
Abra esta pasta no VS Code e execute no terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

A API ficará em http://127.0.0.1:5000. Mantenha esse terminal aberto par# API de Gerenciamento de Tarefas — SW II

## Integrantes

- Miguel Angelo Monteiro Vicente
- Ana Vitória de Oliveira

## Sobre o projeto

Este projeto consiste em uma API REST desenvolvida em Python com Flask, que permite consultar e cadastrar tarefas. A API utiliza autenticação JWT para proteger o cadastro de novas tarefas e realiza a validação dos dados recebidos.

## Tecnologias utilizadas

- Python
- Flask
- Flask-JWT-Extended
- Werkzeug
- Pytest
- Bruno

## Como executar o projeto

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Execute a aplicação:

```powershell
.\.venv\Scripts\python.exe app.py
```

A API estará disponível em `http://127.0.0.1:5000`.

## Credenciais de demonstração

- Usuário: aluno
- Senha: 123456

## Rotas da API

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| POST | /login | Realiza o login e gera um token JWT | Não |
| GET | /tarefas | Lista as tarefas cadastradas | Não |
| POST | /tarefas | Cadastra uma nova tarefa | Sim |

Para cadastrar uma tarefa, é necessário enviar um token JWT válido no cabeçalho Authorization e informar um título no corpo da requisição.

## Testes automatizados

Para executar os testes, utilize:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Os testes verificam o funcionamento do login, a consulta de tarefas, a autenticação no cadastro e a validação de títulos.

Todos os oito testes foram executados com sucesso.

Todos os prints que foram tirados do projeto estão na pasta "prints"

## Conclusão

O desenvolvimento deste projeto permitiu aplicar os conhecimentos adquiridos em aula sobre APIs REST, autenticação JWT, validação de dados e testes automatizados. Os resultados obtidos demonstram que a aplicação atende aos requisitos propostos na atividade.