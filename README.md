# Projeto API FastAPI com Docker

## Como rodar o projeto:

1. Construa a imagem:
   `sudo docker build -t fastapi_app .`

2. Rode o container com rede e volume:
   `sudo docker run -d --name api_container --network api_network -p 8000:8000 -v $(pwd)/data:/app/data fastapi_app`

3. Teste a API:
   `curl http://localhost:8000/`