from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
   return {"mensagem": "Aplicação ativa"}

@app.get("/health")
def health():
   return {"status": "ok"}