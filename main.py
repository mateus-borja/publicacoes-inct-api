from fastapi import FastAPI
from routes.status import entry_root
from routes.publicacao import publicacoes_root
app = FastAPI()

app.include_router(entry_root)
app.include_router(publicacoes_root)