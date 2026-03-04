from fastapi import FastAPI, HTTPException
import os

# Instância principal da aplicação FastAPI.
# Responsável por registrar rotas e configurar o ciclo de vida da aplicação.
app = FastAPI()

# Diretório base para persistência de dados em disco.
# Quando utilizado com Docker, recomenda-se mapear esse diretório para um volume
# externo (-v) para garantir persistência mesmo após reinicialização do container.
DATA_DIR = "data"

# Garante que o diretório de persistência exista no momento da inicialização.
# O parâmetro exist_ok=True evita exceção caso o diretório já exista,
# tornando a operação idempotente.
os.makedirs(DATA_DIR, exist_ok=True)


@app.get("/")
def root():
    """
    Endpoint raiz da aplicação.
    Utilizado como verificação simples de disponibilidade do serviço.
    """
    return {"mensagem": "Aplicação ativa"}


@app.get("/health")
def health():
    """
    Endpoint de verificação de saúde (health check).
    Pode ser utilizado por orquestradores (Docker, Kubernetes, PaaS)
    para monitoramento e reinicialização automática do serviço.
    """
    return {"status": "ok"}


@app.post("/data/{filename}")
def create_file(filename: str, content: str):
    """
    Cria um arquivo no diretório de persistência com o conteúdo informado.

    :param filename: Nome do arquivo a ser criado.
    :param content: Conteúdo textual a ser gravado no arquivo.
    :raises HTTPException 400: Caso o arquivo já exista.
    """

    # Constrói o caminho absoluto do arquivo dentro do diretório de dados.
    file_path = os.path.join(DATA_DIR, filename)

    # Evita sobrescrita acidental de arquivos existentes.
    # Retorna erro 400 (Bad Request) caso o recurso já esteja presente.
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="Arquivo já existe")

    # Abre o arquivo em modo escrita.
    # Caso não exista, será criado automaticamente.
    # O uso do contexto (with) garante fechamento adequado do arquivo.
    with open(file_path, "w") as f:
        f.write(content)

    return {"mensagem": f"Arquivo {filename} criado com sucesso"}


@app.delete("/data/{filename}")
def delete_file(filename: str):
    """
    Remove um arquivo do diretório de persistência.

    :param filename: Nome do arquivo a ser removido.
    :raises HTTPException 404: Caso o arquivo não seja encontrado.
    """

    # Constrói o caminho absoluto do arquivo.
    file_path = os.path.join(DATA_DIR, filename)

    # Verifica existência antes da remoção para evitar erro de sistema.
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    # Remove o arquivo do sistema de arquivos.
    os.remove(file_path)

    return {"mensagem": f"Arquivo {filename} removido com sucesso"}